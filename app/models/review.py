from bson import ObjectId
from .. import mongo


class rate:
    
    def insert_review(review_data):
        
        return  mongo.db.rating_review.insert_one(review_data)
    
    
    def get_product():
        return mongo.db.rating_review.find()
    
    def review_edit(filter_query, update_data):
        return mongo.db.rating_review.update_one(filter_query, update_data)
    
    def review_delete(delete_id):
        return mongo.db.rating_review.delete_one({'_id': ObjectId(delete_id)})