from bson import ObjectId
from .. import mongo

class Users:
  
    def get_user_by_email(Email, Password=None):
        query = {'Email': Email}
        if Password:
            query['Password'] = Password
        return mongo.db.user.find_one(query)

    def register_user(new_user):
        # Check if the user already exists
        existing_user = Users.get_user_by_email(new_user["Email"])
        if existing_user:
            return False  # Indicate that the user already exists
        # Insert user credentials into MongoDB
        mongo.db.user.insert_one(new_user)
        return True  # Indicate that the user was successfully registered

    def get_user_buyer(Email, Password=None):
        query = {'Email': Email}
        if Password:
            query['Password'] = Password
        return mongo.db.user_buyer.find_one(query)

    def register_buyer(new_buyer):
        # Check if the buyer already exists
        existing_buyer = Users.get_user_buyer(new_buyer["Email"])
        if existing_buyer:
            return False  # Indicate that the buyer already exists
        # Insert buyer data into MongoDB
        mongo.db.user_buyer.insert_one(new_buyer)
        return True  # Indicate that the buyer was successfully registered
    
    def landing():
        return mongo.db.enquiry1.find()



    
  

 