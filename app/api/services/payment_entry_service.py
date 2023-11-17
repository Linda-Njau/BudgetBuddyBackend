from ...models import PaymentEntry, PaymentCategory
from ... import db
from datetime import datetime, timedelta
from flask_api import status

def get_error_message(errors, status_code):
    if isinstance(errors, list):
        error_message = '; '.join(errors)
    else:
        error_message = errors
    return {'error': error_message}, status_code

def get_success_message(data, status_code=status.HTTP_200_OK):
    return {'data': data, 'message': 'success'}, status_code

class PaymentEntryService:
    """Service for interacting with the payment entry endpoints"""
    
    def is_valid_payment_entry(self, data, context):
        """Validate payment entry data based on the context."""
        error_messages = []
        if context == 'create' or context == 'update':
            if 'amount' not in data:
                error_messages.append("Amount is missing")
            else:
                try:
                    amount = float(data['amount'])
                    if amount <= 0:
                        error_messages.append("Amount must be positive number.")
                except ValueError:
                    error_messages.append("Invalid amount format. It must be a number.")

            if 'payment_category' not in data:
                error_messages.append("Payment category is missing")
            else:
                valid_categories = [category.value for category in PaymentCategory]
                if data['payment_category'] not in valid_categories:
                    error_messages.append("Invalid payment category")
                    
            if 'transaction_date' not in data:
                error_messages.append("Transaction date is missing")
            else:
                try:
                    datetime.strptime(data['transaction_date'], '%Y-%m-%d').date()                
                except ValueError:
                    error_messages.append("Invalid transaction date format. Use YYYY-MM-DD")
        if context == "patch":
            if 'amount' in data:
                try:
                    amount = float(data['amount'])
                    if amount <= 0:
                        error_messages.append("Amount must be positive number.")
                except ValueError:
                    error_messages.append("Invalid amount format. It must be a number.")
            if 'payment_category' in data:
                valid_categories = [category.value for category in PaymentCategory]
                if data['payment_category'] not in valid_categories:
                    error_messages.append("Invalid payment category")
            if 'transaction_date' in data:
                try:
                    datetime.strptime(data['transaction_date'], '%Y-%m-%d').date()          
                except ValueError:
                    error_messages.append("Invalid transaction date format. Use YYYY-MM-DD")
        if error_messages:
            return False, error_messages
        return True, None
    
    def convert_str_to_date(self, transaction_date_str):
        try:
            return datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
        except ValueError:
            return None
  
    def create_payment_entry(self, data):
        """Create a new payment entry"""
        amount = data.get('amount')
        payment_category_value = data.get('payment_category')
        transaction_date_str = data.get('transaction_date')
        user_id = data.get('user_id')
       
        is_valid, error_response = self.is_valid_payment_entry(data, context='create')
        if not is_valid:
           return get_error_message(error_response, status.HTTP_400_BAD_REQUEST)
        
        transaction_date = self.convert_str_to_date(transaction_date_str)
        payment_category = None
        for enum_member in PaymentCategory:
            if enum_member.value == payment_category_value:
                payment_category = enum_member
                break
        new_payment_entry = PaymentEntry(
            amount=amount,
            payment_category=payment_category,
            transaction_date=transaction_date,
            user_id=user_id
        )
        db.session.add(new_payment_entry)
        db.session.commit()
            
        return get_success_message({"payment_entry_id": new_payment_entry.id}, status.HTTP_201_CREATED)

    def get_payment_entry(self, payment_entry_id):
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
        if not payment_entry:
            return get_error_message("Payment entry not found", status.HTTP_404_NOT_FOUND)
        
        payment_entry_data = {
            'amount': payment_entry.amount,
            'transaction_date': payment_entry.transaction_date.strftime("%Y-%m-%d"),
            'payment_category': payment_entry.payment_category.value
        }
        return payment_entry_data
    
    def get_payment_entries(self, user_id, payment_category=None, month=None, start_date=None, end_date=None):
        """Returns all payment entries for the user by user_id
            filter by payment_category and month if provided
        """
        user_payment_entries_query = PaymentEntry.query.filter_by(user_id=user_id)
        
        if payment_category:
            user_payment_entries_query = user_payment_entries_query.filter(PaymentEntry.payment_category == payment_category)
        if month:
            user_payment_entries_query = user_payment_entries_query.filter(db.func.extract('month', PaymentEntry.transaction_date) == month)
        if start_date and end_date:
            user_payment_entries_query = user_payment_entries_query.filter(PaymentEntry.transaction_date.between(start_date, end_date))
        
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
                return get_error_message("Payment entry not found", status.HTTP_404_NOT_FOUND)
            
            is_valid, error_response = self.is_valid_payment_entry(data, context='update')
            if not is_valid:
                return get_error_message(error_response, status.HTTP_400_BAD_REQUEST)
            
            
           
            transaction_date = self.convert_str_to_date(data.get('transaction_date'))
            payment_entry.update(
            amount=data.get('amount'),
            transaction_date=transaction_date,
            payment_category=data.get('payment_category')
            )
            db.session.commit()
            return get_success_message({"message": "Payment entry updated successfully"}, status.HTTP_200_OK)
        
    def patch_payment_entry(self, payment_entry_id, data):
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
            if not payment_entry:
                return get_error_message("Payment entry not found", status.HTTP_404_NOT_FOUND)
            
            time_elapsed = datetime.utcnow() - payment_entry.created_at
            time_limit = timedelta(hours=24)
            if time_elapsed > time_limit:
                return get_error_message("Payment Entry cannot be edited after 24 hours", status.HTTP_403_FORBIDDEN)
            
            is_valid, error_response = self.is_valid_payment_entry(data, context="patch")
            if not is_valid:
                return get_error_message(error_response, status.HTTP_400_BAD_REQUEST)
            
            if 'amount' in data:
                payment_entry.amount = (data['amount'])
            if 'transaction_date' in data:
                transaction_date = self.convert_str_to_date(data.get('transaction_date'))
                payment_entry.transaction_date = transaction_date
            if 'payment_category' in data:
                payment_entry.payment_category = (data['payment_category'])
            
            db.session.commit()
            return get_success_message({"message": "Payment entry updated successfully"}, status.HTTP_200_OK)

    def delete_payment_entry(self, payment_entry_id):
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
            if not payment_entry:
                return get_error_message("Payment entry not found", status.HTTP_404_NOT_FOUND)
            db.session.delete(payment_entry)
            db.session.commit()
            return get_success_message({"message": "Payment entry was successfully deleted"}, status.HTTP_204_NO_CONTENT)

