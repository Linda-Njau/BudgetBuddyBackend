from ...models import PaymentEntry, PaymentCategory
from ... import db
from datetime import datetime, timedelta

class PaymentEntryService:
    """Service for interacting with the payment entry endpoints"""
    
    def create_payment_entry(self, data):
        """Create a new payment entry"""
        amount = data.get('amount')
        payment_category_value = data.get('payment_category')
        transaction_date_str = data.get('transactionDate')
        user_id = data.get('user_id')  ##needs to be updated to factor in current user
        if not transaction_date_str:
            return {'error': 'Transaction date is missing or empty'}, 400
        try:
            transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
        except ValueError:
            return {'error': 'Invalid transaction date format.Please use YYYY-MM-DD format.'}, 400
        if not amount or not payment_category_value:
            return {'error': 'missing amount or payment category value'}, 400
        
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
    
    def get_payment_entries(self, user_id, payment_category=None, month=None, start_date_str=None, end_date_str=None):
        """Returns all payment entries for the user by user_id
            filter by payment_category and month if provided
        """
        start_date, end_date = None, None
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        
        """print(f"Executing query for user {user_id} with date_range {start_date} to {end_date} and payment_category {payment_category}")"""
        
        user_payment_entries_query = PaymentEntry.query.filter_by(user_id=user_id)
        
        if payment_category:
            user_payment_entries_query = user_payment_entries_query.filter(PaymentEntry.payment_category == payment_category)
        if month:
            user_payment_entries_query = user_payment_entries_query.filter(db.func.extract('month', PaymentEntry.created_at) == month)    
        if start_date and end_date:
            """print(f"Filtering by start_date: {start_date} and end_date: {end_date}")"""
            user_payment_entries_query = user_payment_entries_query.filter(PaymentEntry.created_at.between(start_date, end_date))
        
        user_payment_entries = user_payment_entries_query.all()
        
        payment_entries = [
            {
                "id": payment_entry.id,
                "amount": payment_entry.amount,
                "transaction_date": payment_entry.transaction_date.strftime("%Y-%m-%d"),
                "payment_category": payment_entry.payment_category.value,
            }
            for payment_entry in user_payment_entries
        ]
        return payment_entries
    

    def update_payment_entry(self, payment_entry_id, data):
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
            if not payment_entry:
                return {'error': 'payment entry not found'}, 404
            transaction_date_str = data.get('transaction_date')
            transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
            payment_entry.update(
                amount=data.get('amount'),
                transaction_date=transaction_date,
                payment_category=data.get('payment_category')
            )
            db.session.commit()
    
    def patch_payment_entry(self, payment_entry_id, data):
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
            if not payment_entry:
                return{"message": "Payment Entry not found"}, 404
            
            time_elapsed = datetime.utcnow() - payment_entry.created_at
            time_limit = timedelta(hours=24)
            if time_elapsed > time_limit:
                return {"message": "Payment Entry cannot be edited after 24 hours"}, 403
            
            if 'amount' in data:
                payment_entry.amount = (data['amount'])
            if 'transaction_date' in data:
                payment_entry.transaction_date = (data['transaction_date'])
            if 'payment_category' in data:
                payment_entry.payment_category = (data['payment_category'])
            db.session.commit()
            return {"message": "Payment entry updated successfully"}, 200

    def delete_payment_entry(self, payment_entry_id):
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
            if not payment_entry:
                return {'error': 'Payment entry not found'}, 404
            db.session.delete(payment_entry)
            db.session.commit()
            
            return {'message': 'Payment entry was successfully deleted'}
