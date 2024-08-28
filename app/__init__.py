from flask import Flask
from flask_pymongo import PyMongo
from .config import Config

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # initializes the PyMongo instance with the Flask application, allowing the application to use the MongoDB database.
    mongo.init_app(app)
    
    # register blueprint for signup
    
    with app.app_context():
        # this block used to ensure that the application context is available when registering the application blueprints
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