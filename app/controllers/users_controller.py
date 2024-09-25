from flask import jsonify,request, flash, redirect, url_for, render_template, session
from bson import ObjectId
import re
from ..models.users import Users

def index():
    return render_template('index.html')

def signup():
    if request.method == 'POST':
        Name = request.form['Name']
        Contact = request.form['Contact']
        Email = request.form['Email']
        Password = request.form['Password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if Password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('signup'))

        # Validate email format
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, Email):
            flash('Invalid email format. Please try again.', 'error')
            return redirect(url_for('signup'))

        # Prepare new user data
        new_user = {'Name': Name,'Contact': Contact,'Email': Email,'Password': Password,
        }
        # Register the user and handle the result
        if not Users.register_user(new_user):
            return redirect(url_for('login.signup'))

        return render_template('login.html')
    
    
    
    

    return render_template('signup.html')

def login():
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']

        # Check if the email and password match
        user = Users.get_user_by_email(Email, Password)  # Check the user in the database
        if user:
            
            # Here, l have redirect to a landing 
            return redirect(url_for('login.landing'))

        flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')


def signup_buyer():
    if request.method == 'POST':
        Name = request.form['Name']
        Contact = request.form['Contact']
        Email = request.form['Email']
        Password = request.form['Password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if Password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('signup_buyer'))

        # Prepare new buyer data
        new_buyer = {'Name': Name,'Contact': Contact,'Email': Email,'Password': Password,
        }

        # Register the buyer and handle the result
        if not Users.register_buyer(new_buyer):
            return redirect(url_for('login.signup_buyer'))

        return render_template('login_buyer.html')

    return render_template('signup_buyer.html')


def login_buyer():
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']
        # Check if the email and password match
        buyer = Users.get_user_buyer(Email, Password)  # Check the buyer in the database
        if buyer:
            # If the buyer exists, set a session variable to indicate they are logged in
            # Here, you might also want to redirect to a dashboard or profile page
            return redirect(url_for('catelog_buyer.catelog_buyer'))  # Redirect to the catalog_buyer route

        flash('Invalid email or password. Please try again.', 'error')

    return render_template('login_buyer.html')

def landing():
    car_sell = list(Users.landing())  # Fetch all the data from the landing() method
    count = len(car_sell)
    print("Total records:", count)
    return render_template('car_sell.html', car_sell=car_sell, count=count)
    
    
def about():
    return render_template('about.html')
    

    
   


















