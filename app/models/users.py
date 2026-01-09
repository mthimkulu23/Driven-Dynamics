import email
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
    

    @staticmethod
    def get_messages_by_email(email):
    # This assumes your 'messages' or 'cars' collection has a field called 'RecipientEmail' or 'Email'
    # Replace 'messages' with your actual collection name
     return mongo.db.messages.find({"recipient_email": email})
    




    @staticmethod
    def landing(user_email):
        # We only find enquiries where the 'SellerEmail' matches the logged-in user
        return mongo.db.enquiry1.find({"SellerEmail": user_email})

    @staticmethod
    def save_enquiry(data):
        # This saves the message/enquiry from the buyer
        # 'data' must include 'SellerEmail' so we know who to show it to later
        return mongo.db.enquiry1.insert_one(data)