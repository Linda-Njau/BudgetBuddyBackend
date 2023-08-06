from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from os import path


db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

def create_app():
    """Create a new flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
def create_database(app):
    """Create a database if it doesn't already exist"""
    if not path.exists('app/' + DB_NAME):
        db.create_all()
        print("Database created successfully")

