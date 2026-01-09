from flask import jsonify, request, flash, redirect, url_for, render_template, session, current_app
import re
from flask_socketio import emit, send, join_room, leave_room, disconnect
import flask_socketio as flask_socketio
from .. import socketio

from app.models.enquire import car_enquiry
from ..models.users import Users
from ..models.catelog import User_catelog
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
# app/controllers/users_controller.py

# BUYER LOGIN
def login_buyer():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')

        # Debug logging to trace form submission
        print(f"[DEBUG] /login_buyer POST received. Email={email}")

        # 1. Fetch the buyer from the database using your model logic
        buyer = Users.get_user_buyer(email, password)
        
        if buyer:
            # 2. Set Session (Identical logic to Seller login)
            session['user_id'] = str(buyer['_id'])
            session['user_email'] = buyer['Email']
            session['user_name'] = buyer['Name']
            session['user_role'] = 'buyer'
            
            flash('Login successful! Welcome back!', 'success')
            
            # 3. Redirect to the Buyer Catalog
            # Note: The catalog routes live in the 'catelog_buyer' blueprint.
            return redirect(url_for('catelog_buyer.catelog_buyer'))
            
        else:
            # 4. If login fails, stay on the login page (don't go to catalog)
            print(f"[DEBUG] Buyer login failed for Email={email}")
            flash('Invalid email or password.', 'error')
            return redirect(url_for('users.login_buyer'))
    
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

        print(f"[DEBUG] /login POST received. Email={email}")

        user = Users.get_user_by_email(email, password)
        
        if user:
            session['user_id'] = str(user['_id'])
            session['user_email'] = user['Email']
            session['user_name'] = user['Name']
            session['user_role'] = 'seller'
            flash('Login successful! Welcome back!', 'success')
            return redirect(url_for('users.landing'))  # Change to your seller dashboard route
        else:
            print(f"[DEBUG] Seller login failed for Email={email}")
            flash('Invalid email or password.', 'error')
            return redirect(url_for('users.login'))  # FIXED
    
    return render_template('login.html')






def landing():
    # 1. Security Check: is the user logged in?
    if 'user_email' not in session:
        return redirect(url_for('users.login'))

    # 2. Get the current user's email from the session
    current_email = session['user_email']

    # 3. Use the updated model methods with the email filter
    # car_sell now only contains messages for THIS user
    car_sell = list(car_enquiry.fetch_seller(current_email))
    
    # count now only reflects messages for THIS user
    msg_count = car_enquiry.count_messages_for_user(current_email)

    return render_template('car_sell.html', car_sell=car_sell, count=msg_count)




@socketio.on('message')
def handle_message(msg):
    """Handle incoming chat messages from clients.

    This implements a small intent-detector and a per-socket simple context so
    follow-up replies (e.g. answering "yes" after asking a question) work.
    """
    try:
        # Support messages sent as either plain strings or objects {client_id, text}
        client_id = None
        text = ""
        if isinstance(msg, dict):
            client_id = msg.get('client_id') or 'anon'
            text = str(msg.get('text') or '').strip()
        else:
            text = str(msg or '').strip()
            client_id = 'anon'

        print(f"[CHAT] client={client_id} msg={text}")
        user_msg = text.lower()

        # Per-client in-memory conversation state
        if not hasattr(handle_message, 'conversations'):
            handle_message.conversations = {}
        conv = handle_message.conversations.setdefault(client_id, {})

        # Intent detection
        def detect_intent(u):
            if re.search(r"\b(hi|hello|hey)\b", u):
                return ('greet', None)
            if re.search(r"\b(listings|listings|show listings|list)\b", u):
                return ('listings', None)
            if 'bmw' in u:
                return ('brand_bmw', None)
            if 'polo' in u or 'vw' in u or 'volkswagen' in u:
                return ('brand_polo', None)
            if re.search(r"\b(sell|listing|sell my car|how to sell)\b", u):
                return ('sell_process', None)
            if re.search(r"\b(deal|deals|offer|special)\b", u):
                return ('deals', None)
            if re.search(r"\b(price|cost|how much|pricing)\b", u):
                return ('pricing', None)
            if re.search(r"\b(review|reviews|rate|rating)\b", u):
                return ('reviews', None)
            if re.search(r"\b(contact|phone|email|address|location)\b", u):
                return ('contact', None)
            if u.strip() in ('yes', 'yeah', 'y', 'sure', 'ok'):
                return ('affirm', None)
            if u.strip() in ('no', 'n', 'nah'):
                return ('deny', None)
            return ('unknown', None)

        intent, _ = detect_intent(user_msg)

        # Detect multiple requested topics in a single message (e.g. "listings, reviews, selling my car")
        multi_topics = []
        if re.search(r"\blistings|list\b", user_msg):
            multi_topics.append('listings')
        if re.search(r"\breview|reviews|rating\b", user_msg):
            multi_topics.append('reviews')
        if re.search(r"\bsell|selling|how to sell|listing\b", user_msg):
            multi_topics.append('sell_process')
        if re.search(r"\bdeal|deals|offer|special|price|pricing\b", user_msg):
            multi_topics.append('deals')

        if len(multi_topics) > 1:
            # Build a combined helpful response
            parts = []
            if 'listings' in multi_topics:
                parts.append("Listings — browse the 'Catalog' or tell me a model and I'll show sample listings.")
            if 'reviews' in multi_topics:
                parts.append("Reviews — visit the 'Reviews' page or ask me for a specific model's reviews.")
            if 'sell_process' in multi_topics:
                parts.append("Selling — create a seller account, go to 'Sell Your Car' and submit details and photos.")
            if 'deals' in multi_topics:
                parts.append("Deals — check the 'Deals' section on the homepage for time-limited offers; tell me a model and I'll try to fetch current prices.")

            combined = "I can help with all of those. Quick summary:\n- " + "\n- ".join(parts) + "\nWhich would you like to start with?"
            emit('response', combined)
            return

        # Helper: query inventory for brand/model
        def find_products_for_keyword(kw):
            try:
                products = list(User_catelog.find())
            except Exception as e:
                print(f"[CHAT] inventory lookup error: {e}")
                products = []

            matches = []
            for p in products:
                # fields vary; try make/model/Name
                make = str(p.get('make', '')).lower()
                model = str(p.get('model', '')).lower()
                name = str(p.get('Name', '')).lower()
                if kw in make or kw in model or kw in name:
                    matches.append(p)
            return matches

        response = None

        if intent == 'greet':
            response = "Hello! Welcome to Driven Dynamics. I can help with car listings, reviews, selling your car, or current deals. What would you like to know?"

        elif intent == 'brand_bmw':
            # Search inventory for BMWs
            matches = find_products_for_keyword('bmw')
            if matches:
                # Build a friendly list
                names = []
                for m in matches:
                    mm = m.get('model') or m.get('Name') or f"{m.get('make','')} {m.get('model','') }"
                    names.append(str(mm))
                unique = sorted(list({n for n in names if n}))
                response = f"We currently have the following BMWs available: {', '.join(unique)}. Would you like to see reviews or prices for any of these?"
                conv['last'] = 'brand_bmw'
            else:
                response = "We have BMW models like the M3 and X5 in our catalogue. Would you like to see their reviews or current prices?"
                conv['last'] = 'brand_bmw'

        elif intent == 'brand_polo':
            response = "The VW Polo TSI and Polo Vivo are popular here—great fuel economy and value. Would you like to see specific listings or reviews?"
            conv['last'] = 'brand_polo'

        elif intent == 'listings':
            # If user asked for listings, try to detect a brand/model in the same message
            # e.g., "listings for BMW" or "show Polo listings"
            found = None
            for kw in ('bmw', 'polo', 'toyota', 'ford', 'mercedes'):
                if kw in user_msg:
                    found = kw
                    break

            if found:
                matches = find_products_for_keyword(found)
                if matches:
                    # Show up to 3 sample listings
                    out_lines = []
                    for p in matches[:3]:
                        title = p.get('model') or p.get('Name') or f"{p.get('make','')} {p.get('model','') }"
                        price = p.get('price') or p.get('Price') or 'Price not listed'
                        out_lines.append(f"{title} — {price}")
                    response = "Sample listings:\n" + "\n".join(out_lines)
                else:
                    response = "I couldn't find listings for that model right now. Try another model or visit the Catalog page."
            else:
                conv['last'] = 'awaiting_listings_model'
                response = "Which model or brand would you like listings for? (e.g. 'BMW M3' or 'Polo TSI')"

        elif intent == 'sell_process':
            response = (
                "To sell your car on Driven Dynamics: 1) Create an account and login as a Seller. "
                "2) Go to 'Sell Your Car' and fill in the vehicle details and photos. "
                "3) Set your asking price and submit. Our team will review and your listing goes live. Need help with images or pricing?"
            )

        elif intent == 'deals' or intent == 'pricing':
            response = "Prices and deals change often — check our 'Deals' section on the homepage for the latest offers. If you tell me a model, I can try to fetch current listings and prices."

        elif intent == 'reviews':
            response = "You can view customer reviews under the 'Reviews' page. Tell me a model (e.g. 'BMW M3') and I can summarize reviews for that model."
            # per-socket conversation state disabled

        elif intent == 'contact':
            response = "You can reach Driven Dynamics by email at support@drivendynamics.example or call us at +123-456-7890. Our showroom is open Mon-Fri 9am-5pm."

        elif intent == 'affirm':
            # Without persistent per-socket context, ask a clarifying question
            response = "Thanks — can you tell me which model or question you mean? For example: 'Show BMW M3 reviews' or 'How much is the Polo?'"

        elif intent == 'deny':
            response = "No problem — tell me what you'd like to know. You can ask about models, selling, reviews, or deals."

        else:
            response = "I'm not sure I understand. You can ask about our 'BMW', 'Polo', selling process, or current 'Deals'. Tell me a model name for specific listings."

        if not response:
            response = "Sorry, I couldn't process that. Try asking about a model, selling your car, or current deals."

        emit('response', response)

    except Exception as e:
        print(f"[CHAT ERROR] {e}")
        try:
            emit('response', "Sorry, something went wrong with the chat. Please try again later.")
        except Exception:
            pass


















