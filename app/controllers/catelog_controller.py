from flask import jsonify,request, flash, redirect, url_for, render_template, session  
from ..models.catelog import User_catelog
from .. import mongo
from bson.objectid import ObjectId
import os
from flask import current_app
from ..utils.auth import login_required, role_required
import datetime


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
        # sellers should only see their own products in the edit view
        seller_email = session.get('user_email')
        products = User_catelog.find_by_seller(seller_email)
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
        # ensure only the owner (or admin) can delete
        prod = User_catelog.find_one({'_id': ObjectId(id)})
        user_email = session.get('user_email')
        # allow deletion if owner or admin role (role check performed by decorator in routes)
        if prod and prod.get('SellerEmail') == user_email:
            User_catelog.delete_card(id)
        else:
            # do not delete and optionally flash a message (silent failure for now)
            print(f"Unauthorized delete attempt by {user_email} for product {id}")
        


    return redirect(url_for('catelog_buyer.catelog'))

def catelog():
   
    # public catalog (admin view) - show all products
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
 
    # buyer catalog: only show approved products
    products_cursor = User_catelog.find_approved()

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


@login_required
@role_required('seller')
def seller_my_cars():
    # Show only the cars added by the logged-in seller
    seller_email = session.get('user_email')
    products_cursor = User_catelog.find_by_seller(seller_email)

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
                product['image_url'] = url_for('static', filename='images/img-1-600x400.png')
        else:
            product['image_url'] = url_for('static', filename='images/img-1-600x400.png')
        products.append(product)

    return render_template('seller_cars.html', products=products)


@login_required
@role_required('admin')
def admin_pending():
    # Admin: list products pending verification so they can approve
    pending_cursor = mongo.db.Catelog.find({'status': 'pending_verification'})
    products = []
    uploads_path = os.path.join(current_app.root_path, 'static', 'uploads')
    for p in pending_cursor:
        product = dict(p)
        img = product.get('image')
        if img:
            file_path = os.path.join(uploads_path, img)
            if os.path.exists(file_path):
                product['image_url'] = url_for('static', filename=f'uploads/{img}')
            else:
                product['image_url'] = url_for('static', filename='images/img-1-600x400.png')
        else:
            product['image_url'] = url_for('static', filename='images/img-1-600x400.png')
        products.append(product)

    return render_template('admin_pending.html', products=products)


@login_required
@role_required('admin')
def admin_approve(product_id):
    # Approve a product so it appears in the buyer catalog
    try:
        res = User_catelog.update_one({'_id': ObjectId(product_id)}, {'$set': {'status': 'approved', 'approved_at': datetime.datetime.utcnow()}})
        if hasattr(res, 'modified_count') and res.modified_count > 0:
            flash('Product approved successfully.', 'success')
        else:
            flash('No product was updated. It may already be approved or the id is invalid.', 'warning')
    except Exception as e:
        print(f"Error approving product {product_id}: {e}")
        flash('An error occurred while approving the product.', 'error')
    return redirect(url_for('catelog_buyer.admin_pending'))


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




