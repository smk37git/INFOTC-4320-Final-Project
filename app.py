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
@app.route('/reservations', methods=('GET',))
def reservations_get():
    if request.method == 'GET':
        passengerName = FirstName + LastName
        FirstName = request.form.get('FirstName')
        LastName = request.form.get('LastName')
        SeatRows = request.form.get('SeatRows')
        SeatColumns = request.form.get('SeatColumns')

        # get info for seat reservations:
        dbconnect = sqlite3.connect('reservations.db')
        dbconnect.row_factory = sqlite3.Row
        connection = dbconnect.cursor()

        connection.execute(
            "SELECT * FROM reservations WHERE passengerName=? AND seatRows=? AND seatColumns=? AND eTicketNumber=? AND created=? "
        )

    return render_template('reservations.html')

# ====== Admin Routes ======
@app.route('/admin', methods=('GET','POST'))
def admin_get():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #connection to admin database
        conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "reservations.db"))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute(
            "SELECT * FROM admins WHERE username=? AND password=?", (username,password)
        )
        admin = c.fetchone()
        conn.close()

        if admin: 
            session['admin_logged_in'] = True

            # Get a db connection and create a cursor
            mydb = sqlite3.connect(os.path.join(os.path.dirname(__file__), "reservations.db"))
            mydb.row_factory = sqlite3.Row
            cursor = mydb.cursor()

            # Create and execute a query to get all reservations information
            cursor.execute("SELECT * FROM reservations;")

            # Fetch the results
            reservations = cursor.fetchall()
            mydb.close()

            # Reload page with admin information
            return render_template('admin.html', reservations=reservations)
            
        else:
            flash("Invalid username or password!")            

    return render_template('admin.html')
    
# Run the application
app.run(port=5008, debug=True)