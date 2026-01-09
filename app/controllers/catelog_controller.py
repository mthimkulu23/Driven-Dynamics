from flask import jsonify,request, flash, redirect, url_for, render_template, session  
from ..models.catelog import User_catelog
from bson.objectid import ObjectId
import os
from flask import current_app
from ..utils.auth import login_required, role_required


def viewproduct():
   
    if request.method == 'POST':
        print(request.form['id'])
        id = request.form['id']
        make = request.form['make']
        model = request.form['model']
        mileage = request.form ['mileage']
        description = request.form['description']
        price = request.form['price']
        image = request.form.get('image')

        # If an image filename was provided, build a full static URL for it
        image_url = None
        if image:
            uploads_path = os.path.join(current_app.root_path, 'static', 'uploads')
            file_path = os.path.join(uploads_path, image)
            if os.path.exists(file_path):
                image_url = url_for('static', filename=f'uploads/{image}')
            else:
                print(f"[WARN] viewproduct: image file not found: {file_path}")
                image_url = url_for('static', filename='images/img-1-600x400.png')

        return render_template('view_items.html', id=id, make=make, description=description, price=price,  mileage= mileage, model=model, image=image_url)
    
    
@login_required
@role_required('seller')
def update():
    #retrieve from the database 
    if request.method == 'GET':
        products = User_catelog.find()
        return render_template('catelog.html', products=products)
    elif request.method == 'POST':
        id = request.form['id']
        product = User_catelog.find_one({'_id': ObjectId(id)})
        return render_template('update.html', product=product)
    
    
    
@login_required
@role_required('seller')
def confirm_update():
    id = request.form['id']
    updated_data = {
        'make': request.form['make'],
        'model': request.form['model'],
        'price': request.form['price'],
         'mileage': request.form['mileage'],
        'description': request.form['description'],
        # Add other fields as necessary
    }
    User_catelog.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
    
    products = User_catelog.find()
    return render_template('catelog.html', products=products)
    
    
    
    
    
@login_required
@role_required('seller')
def delete_product():
    # Delete the product from MongoDB
    if request.method == 'POST':
        id = request.form['delete_id']
        User_catelog.delete_card(id)
        

    # Redirect back to the catalog page
    return redirect(url_for('catelog_buyer.catelog'))

def catelog():
    # Retrieve data from MongoDB
    products_cursor = User_catelog.find()

    # Build a list with explicit image URLs and log missing images
    products = []
    uploads_path = os.path.join(current_app.root_path, 'static', 'uploads')
    for p in products_cursor:
        product = dict(p)
        img = product.get('image')
        if img:
            file_path = os.path.join(uploads_path, img)
            if os.path.exists(file_path):
                product['image_url'] = url_for('static', filename=f'uploads/{img}')
            else:
                print(f"[WARN] catelog: image file not found for product {product.get('_id')}: {file_path}")
                product['image_url'] = url_for('static', filename='images/img-1-600x400.png')
        else:
            product['image_url'] = url_for('static', filename='images/img-1-600x400.png')

        products.append(product)

    # Render the catalog template with the data
    return render_template('catelog.html', products=products)
 
def catelog_buyer():
    # Call the model function to get products
    products_cursor = User_catelog.find()

    products = []
    uploads_path = os.path.join(current_app.root_path, 'static', 'uploads')
    for p in products_cursor:
        product = dict(p)
        img = product.get('image')
        if img:
            file_path = os.path.join(uploads_path, img)
            if os.path.exists(file_path):
                product['image_url'] = url_for('static', filename=f'uploads/{img}')
            else:
                print(f"[WARN] catelog_buyer: image file not found for product {product.get('_id')}: {file_path}")
                product['image_url'] = url_for('static', filename='images/img-1-600x400.png')
        else:
            product['image_url'] = url_for('static', filename='images/img-1-600x400.png')

        products.append(product)

    car_buyer = list(User_catelog.buyer_message())  # Fetch all the data from the landing() method
    count = len(car_buyer)
    return render_template('catelog_buyer.html', products=products, car_buyer=car_buyer, count=count)


def buyer_message():
    try:
        buyers = User_catelog.receive_message()
        
        # Handle empty results
        if not buyers:
            buyers = []
            
        return render_template("buyer_message.html", buyers=buyers)
    except Exception as e:
        print(f"Error in buyer_message: {e}")
        # Return empty list on error so page still renders
        return render_template("buyer_message.html", buyers=[], error=str(e))




