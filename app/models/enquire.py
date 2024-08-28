from .. import mongo



class car_enquiry:
    
    def user_enquire(enquiry):
        return  mongo.db.enquiry1.insert_one(enquiry)
    
    
    def fetch_seller():
        return mongo.db.enquiry1.find()
    
    
    def send_seller_message(data):
        return mongo.db.seller_collection.insert_one(data)
    
  
    
    
