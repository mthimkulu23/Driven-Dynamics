from flask import jsonify,request, flash, redirect, url_for, render_template, session  
from ..models.enquire import car_enquiry
from bson .objectid import *

def enquire():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact = request.form['contact']

       
        enquiry = {'name': name,'email': email,'message': message,'contact': contact}
        car_enquiry.user_enquire(enquiry)
        
        return render_template ("catelog_buyer.html")
    else:
        return render_template('enquire.html')
    
def retrieve_seller():
    # Retrieve data from MongoDB
    inquiries = car_enquiry.fetch_seller()
    # Convert the inquiries cursor to a list
    inquiries_list = list(inquiries)

    return render_template('retrieve_seller.html', inquiries=inquiries_list)



def seller_message():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        # Save the form data to the MongoDB collection
        data = { "message": message , "name": name}
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



