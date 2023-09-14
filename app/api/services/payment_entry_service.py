from ...models import PaymentEntry, PaymentCategory
from ... import db
from datetime import datetime

class PaymentEntryService:
    """Service for interacting with the payment entry endpoints"""
    
    def create_payment_entry(self, data):
        """Create a new payment entry"""
        amount = data.get('amount')
        payment_category_value = data.get('payment_category')
        transaction_date_str = data.get('transaction_date')
        user_id = data.get('user_id')  ##needs to be updated to factor in current user
        
        try:
            transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
        except ValueError:
            return {'error': 'Invalid transaction date format.Please use YYYY-MM-DD format.'}, 400
        if not amount or not payment_category_value:
            return {'error': 'missing amount or payment_category_id'}, 400
        
        payment_category = None
        for enum_member in PaymentCategory:
            if enum_member.value == payment_category_value:
                payment_category = enum_member
                break
            
        if not payment_category:
            return {'error': 'invalid payment category'}, 400
        new_payment_entry = PaymentEntry(
            amount=amount,
            payment_category=payment_category,
            transaction_date=transaction_date,
            user_id=user_id
        )
        db.session.add(new_payment_entry)
        db.session.commit()
        
        return{
            "message": "New payment entry added successfully",
            "payment_entry_id": new_payment_entry.id
            }, 201

    def get_payment_entry(self, payment_entry_id):
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
        if not payment_entry:
            return {"error": "payment entry not found"}, 404
        
        formatted_transaction_date = payment_entry.transaction_date.strftime("%Y-%m-%d")
        payment_entry_data = {
            'amount': payment_entry.amount,
            'transaction_date': formatted_transaction_date,
            'payment_category': payment_entry.payment_category.value
        }
        return payment_entry_data
    
    def update_payment_entry(self, payment_entry_id, data):
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
        if not payment_entry:
            return {'error': 'payment entry not found'}, 404
        payment_entry.update(
            amount=data.get('amount'),
            transaction_date=data.get('transaction_date'),
            payment_category=data.get('payment_category')
        )
        db.session.commit()
        return payment_entry.to_dict()
    
    def delete_payment_entry(self, payment_entry_id):
        payment_entry = PaymentEntry.query.get(payment_entry_id)
        if not payment_entry:
            return {'error': 'Payment entry not found'}, 404
        db.session.delete(payment_entry)
        db.session.commit()
        
        return {'message': 'Payment entry was successfully deleted'}
