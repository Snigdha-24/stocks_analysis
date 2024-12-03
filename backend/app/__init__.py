from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from pymongo import MongoClient
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize MongoDB
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client.get_database()
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.stock import stock_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(stock_bp, url_prefix='/api')
    
    return app
