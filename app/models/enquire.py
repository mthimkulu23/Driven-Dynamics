from app import mongo

class car_enquiry:
    
    @staticmethod
    def user_enquire(enquiry):
        # When a buyer sends this, ensure 'SellerEmail' is inside the enquiry dictionary
        return mongo.db.enquiry1.insert_one(enquiry)
    
    @staticmethod
    def fetch_seller(email):
        # Only find enquiries where SellerEmail matches the logged-in user
        return mongo.db.enquiry1.find({"SellerEmail": email})
    
    @staticmethod
    def count_messages_for_user(email):
        # Only count documents belonging to this specific email
        return mongo.db.enquiry1.count_documents({"SellerEmail": email})