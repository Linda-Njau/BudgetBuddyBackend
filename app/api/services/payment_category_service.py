from app.models import PaymentCategory
from app import db

class PaymentCategoryService:
    """Service for interacting with the payment category"""
    
    def get_payment_categories(self, user_id):
        """Returns payment categories for the given user"""
        payment_categories = PaymentCategory.query.filter_by(user_id=user_id).all
