from flask import Flask
from flask_pymongo import PyMongo
from authlib.integrations.flask_client import OAuth  # Add this import
from .config import Config

mongo = PyMongo()
oauth = OAuth()  # Initialize oauth here so it's accessible globally

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    mongo.init_app(app)
    oauth.init_app(app) # Link oauth to the app

    with app.app_context():
        # Import your controller setup function
        from .controllers.users_controller import setup_google_auth
        setup_google_auth(app)

        # Import and register all blueprints
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