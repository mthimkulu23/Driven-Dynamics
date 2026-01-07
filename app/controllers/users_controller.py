from flask import jsonify, request, flash, redirect, url_for, render_template, session
import re
from ..models.users import Users
from authlib.integrations.flask_client import OAuth
from werkzeug.security import check_password_hash

from ..models.users import Users
# IMPORTANT: Import the oauth instance from your app package, don't create a new one!
from .. import oauth


# Initialize OAuth

def setup_google_auth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id='569491132098-tqlmnr3dl0m9tv2ducqte6iuv76jhp2c.apps.googleusercontent.com',
        client_secret='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',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

# app/controllers/users_controller.py



def google_login():
    # Force the redirect URI to 127.0.0.1 to avoid the 'Private IP' error
    # This MUST match exactly what is in your Google Cloud Console
    redirect_uri = "http://127.0.0.1:5000/authorize/google"
    
    print(f"DEBUG: Redirecting to Google with callback: {redirect_uri}")
    return oauth.google.authorize_redirect(redirect_uri)

def google_authorize():
    # Note: Use this function to catch errors
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if user_info:
            email = user_info['email']
            user = Users.get_user_by_email(email)
            if not user:
                Users.register_user({
                    'Name': user_info['name'],
                    'Email': email,
                    'Password': 'OAUTH_USER_EXTERNAL',
                    'Contact': 'N/A'
                })
            
            session['user_id'] = email
            session['name'] = user_info['name']
            return redirect(url_for('login.landing'))
    except Exception as e:
        print(f"Authorize Error: {e}")
        flash("Google authentication failed.", "error")
        
    return redirect(url_for('login.login'))

def google_authorize():
   
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if user_info:
        email = user_info['email']
       
        user = Users.get_user_by_email(email)
        if not user:
           
            Users.register_user({
                'Name': user_info['name'],
                'Email': email,
                'Password': 'OAUTH_USER_EXTERNAL', 
                'Contact': 'N/A'
            })
        
        session['user_id'] = email
        session['name'] = user_info['name']
        return redirect(url_for('login.landing'))
    
    flash("Google authentication failed.", "error")
    return redirect(url_for('login.login'))


def index():
    return render_template('index.html')

def about():
    return render_template('about.html')






# BUYER SIGNUP
def signup_buyer():
    if request.method == 'POST':
        data = {
            'Name': request.form.get('Name'),
            'Contact': request.form.get('Contact'),
            'Email': request.form.get('Email'),
            'Password': request.form.get('Password')
        }
        confirm_password = request.form.get('confirm_password')

        if data['Password'] != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('users.signup_buyer'))  # FIXED

        if not Users.register_buyer(data):
            flash('Email already exists.', 'error')
            return redirect(url_for('users.signup_buyer'))  # FIXED

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('users.login_buyer'))  # FIXED

    return render_template('signup_buyer.html')


# BUYER LOGIN
def login_buyer():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')

        buyer = Users.get_user_buyer(email, password)
        
        if buyer:
            session['user_id'] = str(buyer['_id'])
            session['user_email'] = buyer['Email']
            session['user_name'] = buyer['Name']
            session['user_role'] = 'buyer'
            flash('Login successful! Welcome back!', 'success')
            return redirect(url_for('users.catelog_buyer'))  # Change to your buyer dashboard route
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('users.login_buyer'))  # FIXED
    
    return render_template('login_buyer.html')


# SELLER SIGNUP
def signup():
    if request.method == 'POST':
        data = {
            'Name': request.form.get('Name'),
            'Contact': request.form.get('Contact'),
            'Email': request.form.get('Email'),
            'Password': request.form.get('Password')
        }
        confirm_password = request.form.get('confirm_password')

        if data['Password'] != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('users.signup'))  # FIXED

        if not Users.register_user(data):
            flash('Email already exists.', 'error')
            return redirect(url_for('users.signup'))  # FIXED

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('users.login'))  # FIXED

    return render_template('signup.html')


# SELLER LOGIN
def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')

        user = Users.get_user_by_email(email, password)
        
        if user:
            session['user_id'] = str(user['_id'])
            session['user_email'] = user['Email']
            session['user_name'] = user['Name']
            session['user_role'] = 'seller'
            flash('Login successful! Welcome back!', 'success')
            return redirect(url_for('users.landing'))  # Change to your seller dashboard route
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('users.login'))  # FIXED
    
    return render_template('login.html')






def landing():
    car_sell = list(Users.landing())
    return render_template('car_sell.html', car_sell=car_sell, count=len(car_sell))
    

    
   


















