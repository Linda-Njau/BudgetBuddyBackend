from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class PaymentCategory(Enum):
    FOOD = "FOOD"
    TRAVEL = "TRAVEL"
    UTILITIES = "UTILITIES"
    TRANSPORTATION = "TRANSPORT"
    ENTERTAINMENT = "ENTERTAINMENT"
    
class User(db.Model):
    """User object."""
    __tablename__ ="user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    payments = db.relationship('PaymentEntry', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return dict(user_id=self.user_id, username=self.username, email=self.email)
    
    def update(self, email: str = None, password: str = None, username: str = None):
        if email:
            self.email = email
            
        if password:
            self.password_hash = generate_password_hash(password)
        if username:
            self.username = username
        
   
class PaymentEntry(db.Model):
    """single payment entry"""
    __tablename__ = "payment_entry"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    payment_category = db.Column(SQLEnum(PaymentCategory))

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def to_dict(self):
        payment_category_value = self.payment_category.value if isinstance(self.payment_category, Enum) else self.payment_category
        return dict(id=self.id, amount=self.amount, created_at=self.created_at,
                    updated_at=self.updated_at, transaction_date=self.transaction_date, payment_category=payment_category_value)
        
    def update(self, amount=None, transaction_date=None, payment_category=None):
        if amount:
            self.amount = amount
            
        if transaction_date:
            self.transaction_date = transaction_date
            
        if payment_category:
            self.payment_category = payment_category
