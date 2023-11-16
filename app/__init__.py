from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_apscheduler import APScheduler
from .config import Config
from os import path


db = SQLAlchemy()
scheduler = APScheduler()

from .models import *

DB_NAME = "database.db"
def create_app(environment: str = 'development'):
    """Create a new flask application"""
    app = Flask(__name__)
    environment_config = Config[environment]
    app.config.from_object(environment_config)
    db.init_app(app)
    if environment != 'testing':
        scheduler.init_app(app)
        scheduler.start()
    
    CORS(app)


    from .api.auth import auth
    from .api.users import users
    from .api.payment_entry import payment_entries
    
    
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(payment_entries)
    
    # app.register_blueprint(payment_categories)
    
    @app.before_request
    def before_request():
        print("Requested endpoint:", request.endpoint)
     
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
