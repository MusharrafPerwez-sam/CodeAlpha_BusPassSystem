from flask import Flask, render_template, request, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"  # Use env variable in production

# SQLite connection
def get_db_connection():
    conn = sqlite3.connect('tickets.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            travel_date TEXT NOT NULL,
            seat TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    travel_date = request.form['travel_date']
    seat = request.form['seat']

    conn = get_db_connection()
    conn.execute('INSERT INTO bookings (name, email, travel_date, seat) VALUES (?, ?, ?, ?)',
                 (name, email, travel_date, seat))
    conn.commit()
    conn.close()

    flash("Ticket booked successfully!")
    return render_template('index.html')

@app.route('/bookings')
def bookings():
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)