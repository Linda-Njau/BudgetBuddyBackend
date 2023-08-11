from app.models import PaymentEntry, PaymentCategory
from app import db

class PaymentEntryService:
    """Service for interacting with the payment entry endpoints"""
    
    def create_payment_entry(self, data):
        """Create a new payment entry"""
        amount = data.get('amount')
        payment_category_id = data.get('payment_category_id')
       
        if not amount or not payment_category_id:
            return {'error': 'missing amount or payment_category_id'}, 400
        
        payment_category = PaymentCategory.query.get(payment_category_id)
        if not payment_category:
            return {'error': 'invalid payment category id'}, 400
        new_payment_entry = PaymentEntry(
            amount=amount,
            payment_category_id=payment_category_id
        )
        db.session.add(new_payment_entry)
        db.session.commit()
        
        return{"message": "New payment entry added successfully"}, 201

    def get_payment_entry(self, payment_entry_id):
        payment_entry = PaymentEntry.query.get(payment_entry_id)
        if not payment_entry:
            return {"error": "payment entry not found"}, 404
        payment_entry_data = {
            'id': payment_entry.id,
            'amount': payment_entry.amount,
            'payment_date': payment_entry.payment_date,
            'category_name': payment_entry.payment_category.category_name
        }
        return payment_entry_data
    
    def get_payment_entries(self, payment_category_id):
        payment_entries = PaymentCategory.query.filter_by(payment_category_id=payment_category_id).all()
        if not payment_entries:
            return {"error": "Payment entries not found"}, 404
        payment_entries_list = []
        for payment_entry in payment_entries:
            payment_entries_data = {
                'amount': payment_entry.amount,
                'payment_date': payment_entry.payment_date
            }
            payment_entries_list.append(payment_entries_data)
        return payment_entries_list

    def update_payment_entry(self, payment_entry_id, data):
        payment_entry = PaymentEntry.query.get(payment_entry_id)
        if not payment_entry:
            return {'error': 'payment entry not found'}, 404
        new_amount = data.get('amount')
        new_payment_date = data.get('payment_date')
        new_payment_category_name = data.get('payment_category_name')
        
        if new_amount is not None and new_payment_date is not None:
            payment_entry.amount = new_amount
            payment_entry.payment_date = new_payment_date
            
        if new_payment_category_name is not None:
            new_category = PaymentCategory.query.filter_by(category_name=new_payment_category_name).first()
            if not new_category:
                return {'error': 'Invalid payment category name'}, 400
            payment_entry.payment_category_id = new_category.id
            
        db.session.commit()
        return {'message': 'Payment category was successfully updated'}
    
    def delete_payment_entry(self, payment_entry_id):
        payment_entry = PaymentEntry.query.get(payment_entry_id)
        if not payment_entry:
            return {'error': 'Payment entry not found'}, 404
        db.session.delete(payment_entry)
        db.session.commit()
        
        return {'message': 'Payment entry was successfully deleted'}
