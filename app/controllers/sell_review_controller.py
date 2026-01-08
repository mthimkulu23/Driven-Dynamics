import os
from flask import request, render_template, session, redirect, url_for,flash
from werkzeug.utils import secure_filename
from ..models.catelog import User_catelog

# Define the upload folder path
UPLOAD_FOLDER = 'app/static/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def sell_review():
    if request.method == 'POST':
        
        image = request.files.get('image')
        reg_doc = request.files.get('reg_document') 
        
        # 2. Validate that files exist and aren't empty
        if image and reg_doc and image.filename != '' and reg_doc.filename != '':
            
            # Save Car Image
            img_filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, img_filename))
            
     
            doc_filename = secure_filename(reg_doc.filename)
            reg_doc.save(os.path.join(UPLOAD_FOLDER, doc_filename))
            
           
            products = {
                'image': img_filename,
                'reg_document': doc_filename,
                'vin_number': request.form.get('vin_number', '').upper(),
                'license_plate': request.form.get('license_plate', '').upper(),
                'make': request.form.get('make'),
                'model': request.form.get('model'),
                'price': request.form.get('price'),
                'mileage': request.form.get('mileage'),
                'description': request.form.get('description'),
                'status': 'pending_verification',
                'SellerEmail': session.get('user_email')
            }

          
            User_catelog.add_item(products)

            flash("success_popup") 
            
            return redirect(url_for('sell_review.sell_review')) 
        
        else:
            # Show a warning popup if files are missing
            flash("error_missing_files")
            return redirect(url_for('sell_review.sell_review'))
            
    return render_template('sell_review.html')