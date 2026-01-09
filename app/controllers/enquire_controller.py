from flask import jsonify, request, flash, redirect, url_for, render_template, session  
from ..models.enquire import car_enquiry
from .. import mongo  
from bson.objectid import *
from ..utils.auth import login_required, role_required

def enquire():
    # If buyer arrives from a product page, seller_email and product_id will be in query params
    if request.method == 'GET':
        seller_email = request.args.get('seller_email', '')
        product_id = request.args.get('product_id', '')
        return render_template('enquire.html', seller_email=seller_email, product_id=product_id)

    # POST: store the enquiry and ensure it's tagged with the intended seller
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        contact = request.form.get('contact')
        seller_email = request.form.get('seller_email')
        product_id = request.form.get('product_id')

        enquiry = {
            'name': name,
            'email': email,
            'message': message,
            'contact': contact,
            'SellerEmail': seller_email,
            'ProductID': product_id
        }

        car_enquiry.user_enquire(enquiry)

        return redirect(url_for('catelog_buyer.catelog_buyer'))


@login_required
def retrieve_seller():
    # Show all conversations where the logged-in user is a participant.
    # This makes the inbox symmetric: buyers and sellers see the same threads.
    email = session.get('user_email')

    inquiries = car_enquiry.fetch_by_user(email)
    inquiries_list = list(inquiries)

    return render_template('retrieve_seller.html', inquiries=inquiries_list)


@login_required
def seller_message():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        
        data = {"message": message, "name": name}
        result = car_enquiry.send_seller_message(data)

       
        if result.acknowledged:
            return redirect(url_for('enquire.retrieve_seller'))
        else:
           
            return render_template('seller_message.html', error="Failed to save message")
    else:
        return render_template('seller_message.html')


def terms_condition():
    return render_template('conditions.html')