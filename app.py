# Sebastian Main, Mia Altamirano, Trent Duffey, Ben Cummings | INFOTC-4230
# Final Project

# Import modules
from flask import Flask, render_template, request, flash, url_for, redirect

# ====== Create a flask app object and set app variables ======
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRECT_KEY"] = 'your secret key'
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
@app.route('/admin', methods=('GET',))
def admin_get():

    return render_template('admin.html')
    
# Run the application
app.run(port=5008, debug=True)