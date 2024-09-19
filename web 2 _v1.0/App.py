from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS obiecte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nume TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    obiecte = conn.execute('SELECT * FROM obiecte').fetchall()
    conn.close()
    return render_template('index.html', obiecte=obiecte)


@app.route('/adauga', methods=('GET', 'POST'))
def adauga():
    if request.method == 'POST':
        nume = request.form['nume']
        if nume:
            conn = get_db_connection()
            conn.execute('INSERT INTO obiecte (nume) VALUES (?)', (nume,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('adauga.html')

@app.route('/sterge/<int:id>', methods=('POST',))
def sterge(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM obiecte WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
