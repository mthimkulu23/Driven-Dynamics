from flask import jsonify, request, flash, redirect, url_for, render_template, session  
from ..models.enquire import car_enquiry
from .. import mongo  
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
        
   
        return redirect(url_for('catelog_buyer.catelog_buyer'))
        
    else:
        return render_template('enquire.html')


@login_required
def retrieve_seller():
   
    email = session.get('user_email')

   
    inquiries = car_enquiry.fetch_seller(email)
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