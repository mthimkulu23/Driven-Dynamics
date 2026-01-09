import os


class Config:
    """Application configuration.

    NOTE: Do NOT create an app or SocketIO instance here. This module should only
    contain configuration values. SocketIO is created at the package level in
    `app/__init__.py` to avoid circular imports.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY', 'lkjhgfdsa')

   
    MONGO_URI = os.environ.get(
        'MONGO_URI',
        "mongodb+srv://thabang23mthimkulu_db_user:iF7uaE43Q5vxuGbr@cluster0.szsqgnu.mongodb.net/driven_dynamics?retryWrites=true&w=majority",
    )
    
