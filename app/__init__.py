from flask import Flask
from flask_pymongo import PyMongo
from authlib.integrations.flask_client import OAuth
from flask_socketio import SocketIO
from .config import Config


mongo = PyMongo()
oauth = OAuth()
# Create SocketIO instance at package level. Call `socketio.init_app(app)` in

socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

  
    print(f"🔍 MONGO_URI: {app.config.get('MONGO_URI')}")

  
    mongo.init_app(app)
    oauth.init_app(app)
   
    socketio.init_app(app)

    with app.app_context():
        try:
            # Test MongoDB connection
            mongo.db.command('ping')
            print("✅ MongoDB connected successfully!")
            print(f"✅ Database: {mongo.db.name}")
            print(f"✅ Collections: {mongo.db.list_collection_names()}")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            raise

 
        from .controllers.users_controller import setup_google_auth
        setup_google_auth(app)

       
        from .routes import users_route
        from .routes import sell_review_route
        from .routes import catelog_routes
        from .routes import enquire_routes
        from .routes import review_routes

        app.register_blueprint(users_route.app)
        app.register_blueprint(sell_review_route.app)
        app.register_blueprint(catelog_routes.app)
        app.register_blueprint(enquire_routes.app)
        app.register_blueprint(review_routes.app)

    return app