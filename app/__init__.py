import os
import psycopg2
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_apscheduler import APScheduler
from .config import Config, DevelopmentConfig
from sqlalchemy.exc import ProgrammingError
from os import path


db = SQLAlchemy()
scheduler = APScheduler()
jwt = JWTManager()

from .models import *
def create_app(environment: str = 'development'):
    """Create a new flask application"""
    app = Flask(__name__)
    
    if 'DATABASE_URL' in os.environ:
        environment = 'production'
        
    environment_config = Config.get(environment, DevelopmentConfig)
    app.config.from_object(environment_config)
        
    if environment == 'production':
        DATABASE_URL = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
        
        
    db.init_app(app)
    if environment != 'testing':
        scheduler.init_app(app)
        scheduler.start()
        
    jwt.init_app(app)
    CORS(app)
         
    from .auth import auth
    from .user_endpoints import users
    from .payment_entry_endpoints import payment_entries
    
    
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(payment_entries)
    
    # app.register_blueprint(payment_categories)

    if environment == 'testing':
        with app.app_context():
            DB_NAME = 'database.db'
            if not path.exists('unusual_spending/' + DB_NAME):
                db.create_all()
            
    
    from app.services.scheduled_budget_check import scheduled_budget_check
    if environment != 'testing':
        try:
            with app.app_context():
                scheduled_budget_check(app)
        except ProgrammingError:
            pass
    return app
    
