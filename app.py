# Sebastian Main, Mia Altamirano, Trent Duffey, Ben Cummings | INFOTC-4230
# Final Project

# Import modules
from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3
import os

# ====== Create a flask app object and set app variables ======
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

# ====== Home Routes ======
@app.route('/', methods=('GET',))
def index_get():
    return render_template('index.html')

@app.route('/', methods=('POST',))
def index_post():
    # Get the form data
    option = request.form.get('option')

    # Determine where to direct the application
    if option == "reservations":
        return redirect(url_for('reservations_get'))
    elif option == "admin":
        return redirect(url_for('admin_get'))
    else:
        flash("ERROR: You must choose an option from the menu")
        return redirect(url_for('index_get'))
    
# ====== Reservation Routes ======
@app.route('/reservations', methods=('GET', 'POST'))
def reservations_get():
    # Get info to make a reservation
    if request.method == 'POST':
        FirstName = request.form.get('FirstName', '').strip()
        LastName = request.form.get('LastName', '').strip()
        SeatRow = request.form.get('SeatRows')
        SeatColumn = request.form.get('SeatColumns')

        # Convert to int for seat column and rows
        try:
            SeatRow = int(SeatRow)
            SeatColumn = int(SeatColumn)
        except (TypeError, ValueError):
            flash("You must enter a valid value for the row and column fields.")
            return render_template('reservations.html')

        # get info for seat reservations:
        dbconnect = sqlite3.connect('reservations.db')
        dbconnect.row_factory = sqlite3.Row
        connection = dbconnect.cursor()

    mydb = sqlite3.connect(os.path.join(os.path.dirname(__file__), "reservations.db"))
    mydb.row_factory = sqlite3.Row
    reservations = mydb.cursor().execute('SELECT * FROM reservations;').fetchall()
    mydb.close()

    return render_template('reservations.html', seat_matrix=get_seat_matrix(reservations))


@app.route('/admin/<id>/delete/', methods=('POST',))
def delete_reservation(id):

    # Get a db connection and create a cursor
    mydb = sqlite3.connect(os.path.join(os.path.dirname(__file__), "reservations.db"))
    mydb.row_factory = sqlite3.Row
    cursor = mydb.cursor()

    # Create and execute a query to get all reservations information
    delete_query = "DELETE FROM reservations WHERE id = ?"
    cursor.execute(delete_query, (id,))
    mydb.commit()

    if cursor.rowcount == 0:
        flash("ERROR: Reservation not found.")
    else:
        flash(f"SUCCESS: Reservation {id} deleted.")

    mydb.close()

    return redirect(url_for('admin_get'))

# ====== Admin Routes ======
@app.route('/admin', methods=('GET','POST'))
def admin_get():
    reservations = []
    total_sales = 0
    seat_matrix = []

    if session.get('admin_logged_in'):
        mydb = sqlite3.connect(os.path.join(os.path.dirname(__file__), "reservations.db"))
        mydb.row_factory = sqlite3.Row
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM reservations;")
        reservations = cursor.fetchall()
        mydb.close()

        seat_matrix = get_seat_matrix(reservations)

        cost_matrix = get_cost_matrix()

        for reservation in reservations:
            row = int(reservation['seatRow'])
            col = int(reservation['seatColumn'])

   
            total_sales += cost_matrix[row][col]


    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "reservations.db"))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
        admin = c.fetchone()
        conn.close()

        if admin:
            session['admin_logged_in'] = True
            mydb = sqlite3.connect(os.path.join(os.path.dirname(__file__), "reservations.db"))
            mydb.row_factory = sqlite3.Row
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM reservations;")
            reservations = cursor.fetchall()
            mydb.close()
        else:
            flash("Invalid username or password!")

    return render_template('admin.html', reservations=reservations, total_sales=total_sales, seat_matrix=seat_matrix)

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

def get_seat_matrix(reservations):
    seat_matrix = [[0 for _ in range(4)] for _ in range(12)]

    for reservation in reservations:
        row = int(reservation['seatRow'])
        col = int(reservation['seatColumn'])

        seat_matrix[row][col] = 1
    return seat_matrix
    
# Run the application
app.run(port=5008, debug=True)