from . import db
from datetime import datetime


class User(db.Model):
    """User object."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    
    emails = db.relationship('Email', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    
class Email(db.Model):
    """Email object."""
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(256), nullable=False)
    body = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
class PaymentEntry(db.Model):
    """single payment entry"""
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Datetime, default=datetime.utcnow, nullable=False)
    
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    
    
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), nullable=False)
    
    payment_entries = db.relationship('PaymentEntry', backref='payment', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
