from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from .. import mongo

class Users:
    @staticmethod
    def get_user_by_email(Email, Password=None):
        user = mongo.db.user.find_one({'Email': Email})
        if user and Password:
            # Check the hashed password
            if check_password_hash(user['Password'], Password):
                return user
            return None
        return user

    @staticmethod
    def register_user(new_user):
        if Users.get_user_by_email(new_user["Email"]):
            return False 
        # Hash password before saving
        new_user['Password'] = generate_password_hash(new_user['Password'])
        mongo.db.user.insert_one(new_user)
        return True

    @staticmethod
    def get_user_buyer(Email, Password=None):
        buyer = mongo.db.user_buyer.find_one({'Email': Email})
        if buyer and Password:
            if check_password_hash(buyer['Password'], Password):
                return buyer
            return None
        return buyer

    @staticmethod
    def register_buyer(new_buyer):
        if Users.get_user_buyer(new_buyer["Email"]):
            return False
        # Hash password before saving
        new_buyer['Password'] = generate_password_hash(new_buyer['Password'])
        mongo.db.user_buyer.insert_one(new_buyer)
        return True
    
    @staticmethod
    def landing():
        return mongo.db.enquiry1.find()