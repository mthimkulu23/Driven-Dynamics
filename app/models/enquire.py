from .. import mongo

class car_enquiry:
    
    def user_enquire(enquiry):
        return mongo.db.enquiry1.insert_one(enquiry)
    
    def fetch_seller():
        return mongo.db.enquiry1.find()
    
    def send_seller_message(data):
        return mongo.db.seller_collection.insert_one(data)
    
    # Add this new method
    def count_messages_for_user():
        # Count all messages in the seller_collection
        # If you want to count per user, you'll need to filter by user email/id
        return mongo.db.seller_collection.count_documents({})