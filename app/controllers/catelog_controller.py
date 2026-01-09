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
        seller_email = request.form.get('seller_email')

        image_url = None
        if image:
            uploads_path = os.path.join(current_app.root_path, 'static', 'uploads')
            file_path = os.path.join(uploads_path, image)
            if os.path.exists(file_path):
                image_url = url_for('static', filename=f'uploads/{image}')
            else:
                print(f"[WARN] viewproduct: image file not found: {file_path}")
                image_url = url_for('static', filename='images/img-1-600x400.png')

    # pass seller_email so the view page can link the enquiry back to the correct seller
    return render_template('view_items.html', id=id, make=make, description=description, price=price,  mileage= mileage, model=model, image=image_url, seller_email=seller_email)
    
    
@login_required
@role_required('seller')
def update():
  
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
       
    }
    User_catelog.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
    
    products = User_catelog.find()
    return render_template('catelog.html', products=products)
    
    
    
    
    
@login_required
@role_required('seller')
def delete_product():
  
    if request.method == 'POST':
        id = request.form['delete_id']
        User_catelog.delete_card(id)
        


    return redirect(url_for('catelog_buyer.catelog'))

def catelog():
   
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
                print(f"[WARN] catelog: image file not found for product {product.get('_id')}: {file_path}")
                product['image_url'] = url_for('static', filename='images/img-1-600x400.png')
        else:
            product['image_url'] = url_for('static', filename='images/img-1-600x400.png')

        products.append(product)

   
    return render_template('catelog.html', products=products)
 
def catelog_buyer():
 
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

    car_buyer = list(User_catelog.buyer_message()) 
    count = len(car_buyer)
    return render_template('catelog_buyer.html', products=products, car_buyer=car_buyer, count=count)


def buyer_message():
    try:
        # If the user is logged in, return conversation threads involving them
        from ..models.enquire import car_enquiry
        from flask import session

        user_email = session.get('user_email')
        if user_email:
            buyers = list(car_enquiry.fetch_by_user(user_email))
        else:
            # fallback to existing behavior (all messages)
            buyers = User_catelog.receive_message()

        if not buyers:
            buyers = []

        return render_template("buyer_message.html", buyers=buyers)
    except Exception as e:
        print(f"Error in buyer_message: {e}")
        # Return empty list on error so page still renders
        return render_template("buyer_message.html", buyers=[], error=str(e))




