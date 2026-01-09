import os
import time
import uuid
from flask import jsonify,request, flash, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from ..models.review import rate
from bson.objectid import ObjectId
from ..utils.auth import login_required


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@login_required
def review():
    if request.method == 'POST':
        
        image = request.files.get('image')
        name = request.form.get('name')
        make = request.form.get('make')
        model = request.form.get('model')
        review_text = request.form.get('review_text')
        rating = request.form.get('rating')

        image_filename = None
        if image and image.filename:
            image_filename = secure_filename(f"{int(time.time())}_{uuid.uuid4().hex}_{image.filename}")
            image.save(os.path.join(UPLOAD_FOLDER, image_filename))

       
        review_data = {
            'image': image_filename,
            'name': name,
            'make': make,
            'model': model,
            'review_text': review_text,
            'rating': int(rating) if rating else None,
            'author': session.get('user_email')
        }
        rate.insert_review(review_data)
       
        return redirect(url_for('review.review'))

    return render_template('review.html')

def review_display12():

    display = rate.get_product()
    
   
    return render_template('review_display12.html', display=display)

@login_required
def edit_review():
    data = request.json
    edit_id = data.get('edit_id')
    name = data.get('name')
    model = data.get('model')
    make = data.get('make')
    review_text = data.get('review_text')
    rating = data.get('rating')

    if edit_id and name and model and make and review_text and rating:
        result = rate.review_edit(
            {'_id': ObjectId(edit_id)},
            {'$set': {'name': name, 'model': model, 'make': make, 'review_text': review_text, 'rating': rating}}
        )
        if result.modified_count > 0:
            return jsonify({'message': 'Review updated successfully'}), 200
        else:
            return jsonify({'message': 'Review not found or no changes made'}), 404
    return render_template('review_display12.html')

@login_required
def delete_review():
    delete_id = request.form.get('delete_id')
    
    if delete_id:
        result = rate.review_delete(delete_id)
        if result.deleted_count > 0:
            return redirect(url_for('review.review_display12'))
        else:
            return ('Error: Review not found', 'danger')
    else:
        return ('Error: Review not found', 'danger')
    