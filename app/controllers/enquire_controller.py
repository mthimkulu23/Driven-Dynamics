from flask import jsonify, request, flash, redirect, url_for, render_template, session  
from ..models.enquire import car_enquiry
from .. import mongo  # Add this to access products collection
from bson.objectid import *

def enquire():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact = request.form['contact']

        enquiry = {'name': name, 'email': email, 'message': message, 'contact': contact}
        car_enquiry.user_enquire(enquiry)
        
        # Redirect to catalog_buyer route instead of rendering template
        # This will use the existing catalog_buyer controller which already has the logic
        return redirect(url_for('catelog_buyer.catelog_buyer'))
        
    else:
        return render_template('enquire.html')


def retrieve_seller():
    # 1. Get the logged-in seller's email from the session
    # Make sure 'user_email' is the key you used in your login function!
    email = session.get('user_email')

    # 2. Safety check: If they aren't logged in, redirect them
    if not email:
        flash("Please log in to view your inquiries.", "error")
        return redirect(url_for('users.login'))

    # 3. Pass the email into the function (Fixes the TypeError)
    inquiries = car_enquiry.fetch_seller(email)
    
    # 4. Convert the MongoDB cursor to a list for the template
    inquiries_list = list(inquiries)

    return render_template('retrieve_seller.html', inquiries=inquiries_list)


def seller_message():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        # Save the form data to the MongoDB collection
        data = {"message": message, "name": name}
        result = car_enquiry.send_seller_message(data)
        
        # Check if the data was saved successfully
        if result.acknowledged:
            return redirect(url_for('enquire.retrieve_seller'))
        else:
            # Handle the case when the data couldn't be saved
            return render_template('seller_message.html', error="Failed to save message")
    else:
        return render_template('seller_message.html')


def terms_condition():
    return render_template('conditions.html')