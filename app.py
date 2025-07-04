import os
import psycopg2
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        port=os.environ.get('DB_PORT', 5432)
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('name')
    email = request.form.get('email')
    travel_date = request.form.get('travel_date')
    seat = request.form.get('seat')

    if not all([name, email, travel_date, seat]):
        flash("All fields are required.")
        return redirect('/')

    price = 100.0  # Fixed price

    conn = get_db_connection()
    cur = conn.cursor()

    # Create table if not exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            travel_date TEXT,
            seat TEXT,
            price REAL
        )
    ''')

    # Check if seat already booked
    cur.execute('SELECT * FROM bookings WHERE travel_date = %s AND seat = %s', (travel_date, seat))
    if cur.fetchone():
        conn.close()
        flash(f"Seat {seat} is already booked for {travel_date}.")
        return redirect('/')

    # Insert booking
    cur.execute('INSERT INTO bookings (name, email, travel_date, seat, price) VALUES (%s, %s, %s, %s, %s)',
                (name, email, travel_date, seat, price))
    conn.commit()
    conn.close()

    flash("Ticket booked successfully!")
    return redirect('/bookings')

@app.route('/bookings')
def bookings():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM bookings ORDER BY id DESC')
    all_data = cur.fetchall()
    conn.close()
    return render_template('bookings.html', bookings=all_data)

if __name__ == '_main_':
    app.run(debug=True)