from app.api.payment_entry import delete_payment_entry
from app.models import PaymentCategory
from app import db

class PaymentCategoryService:
    """Service for interacting with the payment category"""
    
    def update_payment_category(self, payment_category_id, data):
        payment_category = PaymentCategory.query.get(payment_category_id)
        if not payment_category:
            return {'error': 'Payment category not found'}, 404
        new_category_name = data.get('category_name')
        if not new_category_name:
            return {'error': 'category name is missing'}, 400
        
        existing_category = PaymentCategory.query.filter_by(
            user_id=payment_category.user_id,
            category_name=new_category_name
        ).first()
        if existing_category and existing_category.id != payment_category.id:
            return {'error': 'Category already exists'}, 400
        payment_category.category_name = new_category_name
        db.session.commit()

    def delete_payment_category(self, payment_category_id):
        payment_category = PaymentCategory.query.get(payment_category_id)
        if not payment_category:
            return {'error': 'payment category not found'}, 404
        for payment_entry in payment_category.payment_entries:
            db.session.delete(payment_entry)
        db.session.delete(payment_category)
        db.session.commit()
        return {'error': 'payment category was successfully deleted'}
