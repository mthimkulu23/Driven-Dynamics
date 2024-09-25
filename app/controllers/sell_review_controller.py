from flask import request,render_template 
from ..models.catelog import User_catelog




def sell_review():
    if request.method == 'POST':
        image = request.files['image']
        make = request.form['make']
        model = request.form['model']
        price = request.form['price']
        mileage = request.form['mileage']
        description = request.form['description']

        # Create a dictionary with the correct mileage value
        products = {
            'image': image.filename,'make': make,'model': model,'price': price,'mileage': mileage, 'description': description}

        # Add the product to the catalog
        User_catelog.add_item(products)

        # Redirect to the catalog page after successful submission
        allproducts = User_catelog.find()
    
        return render_template('catelog.html', products=allproducts)
    else:
        return render_template('sell_review.html')
  
