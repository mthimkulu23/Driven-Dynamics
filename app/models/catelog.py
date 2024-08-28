from bson import ObjectId
from .. import mongo


# Model
class User_catelog:
        
        def find():
        # Retrieve data from MongoDB
                products = mongo.db.Catelog.find()
                return products

        def find_buyer():
        # Retrieve data from MongoDB
                products = mongo.db.Catelog.find()
                return products
    
        def delete_card(delete_id):
                #Deletes a product from the 'Catelog' collection in the MongoDB database.
                return mongo.db.Catelog.delete_one({"_id": ObjectId(delete_id)})
   
 
        def add_item(products):   
        #Inserts a new product into the 'Catelog' collection in the MongoDB database.
                return  mongo.db.Catelog.insert_one(products)
        
        def find():
                #Retrieves all products from the 'Catelog' collection in the MongoDB database.
                return mongo.db.Catelog.find()
        
        def find_one(filter):
                #Retrieves a single product from the 'Catelog' collection in the MongoDB database.
                return mongo.db.Catelog.find_one(filter)
        
        
        def update_one(filter, update):
                #Updates a single product in the 'Catelog' collection in the MongoDB database.
                return mongo.db.Catelog.update_one(filter, update)
        
        
        def receive_message():
                #Retrieves all messages from the 'seller_collection' collection in the MongoDB database.
                return list(mongo.db.seller_collection.find())
        
        
        def put_review(review_data):
                #Inserts a new review into the 'rating_review' collection in the MongoDB database.
                return mongo.db.rating_review.insert_one(review_data)
        
        def buyer_message():
                #Retrieves all messages from the 'seller_collection' collection in the MongoDB database.
                return mongo.db.seller_collection.find()

