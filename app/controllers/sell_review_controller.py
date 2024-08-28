from flask import request,render_template 
from ..models.catelog import User_catelog




def sell_review():
    if request.method == 'POST':
        image = request.files['image']
        make = request.form['make']
        model = request.form['model']
        price = request.form['price']
        description = request.form['description']

        # Perform further processing with the form data
        # Example: Save the image, store the car details in a database
        products = {'image': image.filename,'make': make,'model': model,'price': price,'description': description
        }
        User_catelog.add_item(products)
        # Redirect to the catalog page after successful submission
        allproducts = User_catelog.find()
    
        return render_template('catelog.html', products=allproducts)
    else:
        return render_template('sell_review.html')
  
