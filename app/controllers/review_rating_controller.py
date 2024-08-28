from flask import jsonify,request, flash, redirect, url_for, render_template, session  
from ..models.review import rate
from bson .objectid import *

def review():
    if request.method == 'POST':
        # Get the review data from the request
        image = request.files['image']
        name = request.form['name']
        make = request.form['make']
        model = request.form['model']
        review_text = request.form['review_text']
        rating = request.form['rating']
        
        # Save the review data to the MongoDB database
        review_data = {'image': image.filename,'name': name,'make': make,'model': model,'review_text': review_text,'rating': int(rating)}
        rate.insert_review(review_data)
        # Redirect to the same page after submission to clear the form
        return redirect(url_for('review.review'))
    # Render the review template on GET request
    return render_template('review.html')

def review_display12():
    # Retrieve data from MongoDB
    display = rate.get_product()
    
    # Render the catalog template with the data
    return render_template('review_display12.html', display=display)

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
    