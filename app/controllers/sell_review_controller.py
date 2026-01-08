import os
from flask import request, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename
from ..models.catelog import User_catelog

# Define where you want to save the images
UPLOAD_FOLDER = 'app/static/uploads'
# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def sell_review():
    if request.method == 'POST':
        image = request.files['image']
        
        if image:
            # 1. Secure the filename and save the file to the uploads folder
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            
            # 2. Collect form data
            make = request.form['make']
            model = request.form['model']
            price = request.form['price']
            mileage = request.form['mileage']
            description = request.form['description']
            
            # IMPORTANT: Capture the seller's email from the session 
            # so we know who owns this car!
            seller_email = session.get('user_email')

            products = {
                'image': filename,  # Save ONLY the filename in DB
                'make': make,
                'model': model,
                'price': price,
                'mileage': mileage, 
                'description': description,
                'SellerEmail': seller_email # Identification key
            }

            # 3. Add to Database
            User_catelog.add_item(products)

            return redirect(url_for('sell_review.catelog')) # Redirect after post
            
    return render_template('sell_review.html')