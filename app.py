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

    return render_template('reservations.html')

# ====== Admin Routes ======
@app.route('/admin', methods=('GET','POST'))
def admin_get():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #connection to admin database
        conn = sqlite3.connect('reservations.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute(
            "SELECT * FROM admins WHERE username=? AND password=?", (username,password)
        )
        admin = c.fetchone()
        conn.close()

        if admin:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('admin_get'))
        else:
            flash("Invalid username or password!")
        render_template('admin.html')
            

    return render_template('admin.html')

@app.route('/admin', methods=('POST',))
def admin_post():
    username = request.form.get('username')
    password = request.form.get('password')
    admin_usr = "asd" #will come from db  
    admin_pass = 123 #will come from db

    if username == admin_usr and int(password) == admin_pass:
        return render_template('admin_dashboard.html')
    else:
        flash("Invalid username or password!!")
        return redirect(url_for("admin_get"))

    
# Run the application
app.run(port=5008, debug=True)