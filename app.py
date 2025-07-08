from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# HTML template (simple inline version for demonstration)
form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Bus Ticket Booking</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; }
        form { max-width: 400px; }
        input, label { display: block; width: 100%; margin-bottom: 15px; }
        input[type="submit"] {
            background-color: green;
            color: white;
            padding: 10px;
            border: none;
            cursor: pointer;
        }
        a { color: blue; text-decoration: none; }
        .message { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h2>Book Your Ticket</h2>
    {% if message %}
        <p class="message">{{ message }}</p>
    {% endif %}
    <form method="POST" action="/book">
        <label>Name:</label>
        <input type="text" name="name" required>

        <label>Email:</label>
        <input type="email" name="email" required>

        <label>Travel Date:</label>
        <input type="date" name="travel_date" required>

        <label>Seat Number:</label>
        <input type="text" name="seat" required>

        <input type="submit" value="Book Ticket">
    </form>
    <br>
    <a href="/bookings">View All Bookings</a>
</body>
</html>
"""

bookings_html = """
<!DOCTYPE html>
<html>
<head>
    <title>All Bookings</title>
</head>
<body>
    <h2>All Bookings</h2>
    <table border="1" cellpadding="10">
        <tr><th>Name</th><th>Email</th><th>Travel Date</th><th>Seat</th></tr>
        {% for booking in bookings %}
            <tr>
                <td>{{ booking['name'] }}</td>
                <td>{{ booking['email'] }}</td>
                <td>{{ booking['travel_date'] }}</td>
                <td>{{ booking['seat'] }}</td>
            </tr>
        {% endfor %}
    </table>
    <br>
    <a href="/">Back to Booking</a>
</body>
</html>
"""

# SQLite connection
def get_db_connection():
    conn = sqlite3.connect('tickets.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the table on first run
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

# Home page
@app.route('/')
def home():
    return render_template_string(form_html)

# Booking handler
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

    return render_template_string(form_html, message="Ticket booked successfully!")

# View all bookings
@app.route('/bookings')
def bookings():
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return render_template_string(bookings_html, bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)