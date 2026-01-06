from flask import jsonify, request, flash, redirect, url_for, render_template, session
import re
from ..models.users import Users
from authlib.integrations.flask_client import OAuth
from .. import oauth


# Initialize OAuth
oauth = OAuth()

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

from flask import jsonify, request, flash, redirect, url_for, render_template, session
import re
from ..models.users import Users
# IMPORTANT: Import the oauth instance from your app package, don't create a new one!
from .. import oauth 

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

def signup():
    if request.method == 'POST':
        # Your HTML uses Name, Contact, Email, Password, confirm_password
        data = {
            'Name': request.form.get('Name'),
            'Contact': request.form.get('Contact'),
            'Email': request.form.get('Email'),
            'Password': request.form.get('Password')
        }
        confirm_password = request.form.get('confirm_password')

        if data['Password'] != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('login.signup')) # Assuming blueprint name is 'login'

        if not Users.register_user(data):
            flash('Email already exists.', 'error')
            return redirect(url_for('login.signup'))

        flash('Registration successful!', 'success')
        return redirect(url_for('login.login'))

    return render_template('signup.html')

def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')

        user = Users.get_user_by_email(email, password)
        if user:
            session['user_id'] = str(user['_id'])
            session['role'] = 'seller'
            return redirect(url_for('login.landing'))

        flash('Invalid email or password.', 'error')
    return render_template('login.html')

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
            flash('Passwords do not match!', 'error')
            return redirect(url_for('login.signup_buyer'))

        if not Users.register_buyer(data):
            flash('Account already exists.', 'error')
            return redirect(url_for('login.signup_buyer'))

        flash('Buyer account created!', 'success')
        return redirect(url_for('login.login_buyer'))

    return render_template('signup_buyer.html')

def login_buyer():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')
        
        buyer = Users.get_user_buyer(email, password)
        if buyer:
            session['user_id'] = str(buyer['_id'])
            session['role'] = 'buyer'
            return redirect(url_for('catelog_buyer.catelog_buyer'))

        flash('Invalid credentials.', 'error')
    return render_template('login_buyer.html')

def landing():
    car_sell = list(Users.landing())
    return render_template('car_sell.html', car_sell=car_sell, count=len(car_sell))
    

    
   


















