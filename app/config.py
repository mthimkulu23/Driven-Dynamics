import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'lkjhgfdsa')
    
    # Read from environment variable first, fallback for local
    MONGO_URI = os.environ.get('MONGO_URI', 
        "mongodb+srv://thabang23mthimkulu_db_user:iF7uaE43Q5vxuGbr@cluster0.szsqgnu.mongodb.net/driven_dynamics?retryWrites=true&w=majority"
    )
    
