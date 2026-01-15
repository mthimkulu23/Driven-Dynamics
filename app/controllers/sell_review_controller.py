import os
import time
import uuid
from flask import request, render_template, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from ..models.catelog import User_catelog
from ..utils.auth import login_required, role_required_any

# Compute upload folder relative to the package root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@login_required
@role_required_any('seller', 'admin')
def sell_review():
    if request.method == 'POST':
        image = request.files.get('image')
        reg_doc = request.files.get('reg_document')

        
        if image and reg_doc and image.filename and reg_doc.filename:
        
            timestamp = int(time.time())
            img_filename = secure_filename(f"{timestamp}_{uuid.uuid4().hex}_{image.filename}")
            image.save(os.path.join(UPLOAD_FOLDER, img_filename))

            doc_filename = secure_filename(f"{timestamp}_{uuid.uuid4().hex}_{reg_doc.filename}")
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
            # after adding, send the seller to their own cars page so they only see their listings
            return redirect(url_for('catelog_buyer.seller_my_cars'))
        else:
         
            flash("error_missing_files")
            return redirect(url_for('sell_review.sell_review'))

    return render_template('sell_review.html')
