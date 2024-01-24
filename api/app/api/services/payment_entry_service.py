from ...models import PaymentEntry, PaymentCategory, User
from ... import db
from datetime import datetime, timedelta
from flask_api import status

def get_error_message(errors, status_code):
    """
    Create a standardized error response.
    
    Args:
        errors (str or list): A single error message or a list of error messages.
        status_code (int): The HTTP status code associated with the error.

    Returns:
        dict: A dictionary containing the error message(s) and the corresponding status code.
    """
    if isinstance(errors, list):
        error_message = '; '.join(errors)
    else:
        error_message = errors
    return {'error': error_message}, status_code

class PaymentEntryService:
    """Service for interacting with the payment entry endpoints"""
    
    def is_valid_payment_entry(self, data, context):
        """
        Validate the data for a payment entry based on the given context (create, update, patch).

        Args:
            data (dict): The data dictionary to validate.
            context (str): The context in which the validation is being performed ('create', 'update', 'patch').

        Returns:
            tuple: A tuple containing a boolean indicating validity and a list of error messages, if any.
        """
        error_messages = []

        if context == 'create' or context == 'update':
            if 'amount' not in data:
                error_messages.append("Please provide a valid amount")
            else:
                try:
                    amount = float(data['amount'])
                    if amount <= 0:
                        error_messages.append("Amount must be positive number.")
                except ValueError:
                    error_messages.append("Invalid amount format. It must be a number.")

            if 'payment_category' not in data:
                error_messages.append("Please provide a payment category")
            else:
                valid_categories = [category.value for category in PaymentCategory]
                if data['payment_category'] not in valid_categories:
                    error_messages.append("Invalid payment category")
                    
            if 'transaction_date' not in data:
                error_messages.append("Please provide a transaction date")
            else:
                try:
                    datetime.strptime(data['transaction_date'], '%Y-%m-%d').date()                
                except ValueError:
                    error_messages.append("Invalid transaction date format. Use YYYY-MM-DD")
                    
        elif context == "patch":
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
        """
        Convert a date string to a datetime.date object.

        Args:
            transaction_date_str (str): The date string to convert.

        Returns:
            datetime.date: The converted date object, or None if the conversion fails.
        """
        try:
            return datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
        except ValueError:
            return None
  
    def create_payment_entry(self, data):
        """
        Create a new payment entry with the given data.

        Args:
            data (dict): The data for the new payment entry.

        Returns:
            tuple: A success message with the new payment entry's ID, or an error message.
        """
        amount = data.get('amount')
        payment_category_value = data.get('payment_category')
        transaction_date_str = data.get('transaction_date')
        user_id = data.get('user_id')
        
        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
            return get_error_message('User not found', status.HTTP_404_NOT_FOUND)
        
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
            
        return {"payment_entry_id": new_payment_entry.id}, status.HTTP_201_CREATED

    def get_payment_entry(self, payment_entry_id):
        """
        Retrieve a single payment entry by its ID.

        Args:
            payment_entry_id (int): The ID of the payment entry to retrieve.

        Returns:
            dict: A dictionary containing the payment entry's details if found.
            tuple: An error message and a status code if the payment entry is not found.
        """
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
        if not payment_entry:
            return get_error_message("Payment entry not found", status.HTTP_404_NOT_FOUND)
        
        payment_entry_data = {
            'amount': payment_entry.amount,
            'transaction_date': payment_entry.transaction_date.strftime("%Y-%m-%d"),
            'payment_category': payment_entry.payment_category.value
        }
        return payment_entry_data, status.HTTP_200_OK
    
    def get_payment_entries(self, user_id, payment_category=None, month=None, start_date=None, end_date=None):
        """
        Retrieve all payment entries for a specific user, optionally filtering by payment category, 
        month, or a date range.

        Args:
            user_id (int): The user ID for whom the payment entries are to be retrieved.
            payment_category (PaymentCategory, optional): The category of payments to filter by. Default is None.
            month (int, optional): The month number (1-12) to filter the payment entries. Default is None.
            start_date (date, optional): The start date for filtering payment entries. Default is None.
            end_date (date, optional): The end date for filtering payment entries. Default is None.

        Returns:
            list: A list of dictionaries, each representing a payment entry matching the criteria.
        """
        with db.session() as session:
            user = session.get(User, user_id)
            if not user:
                return get_error_message('User not found', status.HTTP_404_NOT_FOUND)
            
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
        if not payment_entries:
            return get_error_message("No payment entries for this user", status.HTTP_404_NOT_FOUND)
        return (payment_entries), status.HTTP_200_OK
    

    def update_payment_entry(self, payment_entry_id, data):
        """
        Update a payment entry with the given data based on the payment entry's ID.

        Args:
            payment_entry_id (int): The ID of the payment entry to be updated.
            data (dict): A dictionary containing the updated fields of the payment entry.

        Returns:
            tuple: A success message upon successful update or an error message if the update fails.
        """
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
            updated_payment_entry = payment_entry.to_dict()
            return updated_payment_entry, status.HTTP_200_OK
        
    def patch_payment_entry(self, payment_entry_id, data):
        """
        Partially update a payment entry based on the payment entry's ID. Only the fields 
        provided in the data dictionary will be updated.

        Args:
            payment_entry_id (int): The ID of the payment entry to be updated.
            data (dict): A dictionary containing the fields to be updated.

        Returns:
            tuple: A success message upon successful update or an error message if the update fails.
        """
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
            if not payment_entry:
                return get_error_message("Payment entry not found", status.HTTP_404_NOT_FOUND)
            
            time_elapsed = datetime.utcnow() - payment_entry.created_at
            time_limit = timedelta(hours=24)
            if time_elapsed > time_limit:
                return get_error_message("Payment Entry cannot be edited after 24 hours", status.HTTP_403_FORBIDDEN)
            
            is_valid, error_response = self.is_valid_payment_entry(data, context='patch')
            if not is_valid:
                return get_error_message(error_response, status.HTTP_400_BAD_REQUEST)
            
            if 'amount' in data:
                payment_entry.amount = (data['amount'])
            if 'transaction_date' in data:
                transaction_date = self.convert_str_to_date(data.get('transaction_date'))
                payment_entry.transaction_date = transaction_date
            if 'payment_category' in data:
                payment_entry.payment_category = (data['payment_category'])
            patched_payment_entry = payment_entry.to_dict()
            db.session.commit()
            return patched_payment_entry, status.HTTP_200_OK

    def delete_payment_entry(self, payment_entry_id):
        """
        Delete a payment entry based on the payment entry's ID.

        Args:
            payment_entry_id (int): The ID of the payment entry to be deleted.

        Returns:
            tuple: A success message upon successful deletion or an error message if the deletion fails.
        """
        with db.session() as session:
            payment_entry = session.get(PaymentEntry, payment_entry_id)
            if not payment_entry:
                return get_error_message("Payment entry not found", status.HTTP_404_NOT_FOUND)
            db.session.delete(payment_entry)
            db.session.commit()
            return "payment entry deleted successfully", status.HTTP_204_NO_CONTENT

