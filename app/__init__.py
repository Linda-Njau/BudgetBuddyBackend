import os
import psycopg2
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_apscheduler import APScheduler
from .config import Config, DevelopmentConfig
from os import path


db = SQLAlchemy()
scheduler = APScheduler()

from .models import *

DB_NAME = "database.db"
def create_app(environment: str = 'development'):
    """Create a new flask application"""
    app = Flask(__name__)
    
    if 'DATABASE_URL' in os.environ:
        environment = 'production'
        
    environment_config = Config.get(environment, DevelopmentConfig)
    app.config.from_object(environment_config)
    
    print(f"Environment: {environment}")
        
    if environment == 'production':
        DATABASE_URL = os.environ.get('DATABASE_URL?sslmode=require').replace('postgres://', 'postgresql://')
        print(f"--------------DATABASE_URL: {DATABASE_URL}")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
        print("Production environment configured.")
        
        
    db.init_app(app)
    if environment != 'testing':
        scheduler.init_app(app)
        scheduler.start()
    
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
            create_database(app)
    
    from scheduled_budget_check import scheduled_budget_check
    if environment != 'testing':
        with app.app_context():
            scheduled_budget_check(app)
    return app

def create_database(app):
    """Create a database if it doesn't already exist"""
    if not path.exists('unusual_spending/' + DB_NAME):
        db.create_all()
