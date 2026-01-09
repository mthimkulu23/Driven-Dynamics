from flask import jsonify, request, flash, redirect, url_for, render_template, session  
from ..models.enquire import car_enquiry
from .. import mongo  # Add this to access products collection
from bson.objectid import *
from ..utils.auth import login_required, role_required

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


@login_required
def retrieve_seller():
    # Get the logged-in seller's email from the session
    email = session.get('user_email')

    # Pass the email into the function
    inquiries = car_enquiry.fetch_seller(email)
    inquiries_list = list(inquiries)

    return render_template('retrieve_seller.html', inquiries=inquiries_list)


@login_required
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