from werkzeug.security import generate_password_hash
from ...models import User, PaymentCategory, PaymentEntry
from ... import db

class UserService:
    """Service for interacting with the users endpoints."""
    
    def create_user(self, data):
        """Creates new user"""
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        
        if not email or not password or not username:
            return {'error': 'missing required fields'}, 400
        
        password_hash = generate_password_hash(password)
        
        new_user = User(
            email=email,
            username=username,
            password_hash=password_hash
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        
            print(f"User {username} created successfully") 
            return {'message' : "Successfully created"}, 201
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user {username}: {str(e)}")
            return {'message' : 'Error creating user'}, 500
    
    def get_user(self, user_id):
        """Returns user information by user_id"""
        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        user_data = {
            'user_id' : user.user_id,
            'email' : user.email,
            'username' : user.username
        }
        return user_data

    def update_user(self, user_id, data):
        """update users by user_id"""
        with db.session() as session:
            user = session.get(User, user_id)
            if not user:
                return {'error': 'User not found'}, 404
            user.update(
                email=data.get('email'),
                password=data.get('password'),
                username=data.get('username')
            )
            db.session.commit()
            return user.to_dict()
    
    def delete_user(self, user_id):
        """Delete a user by id."""
        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
            return {'error' : 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        
        return {'message': 'User deleted successfully'}

    def get_payment_entries(self, user_id, payment_category=None, month=None):
        """Returns all payment entries for the user by user_id
            filter by payment_category and month if provided
        """
        user_payment_entries_query = PaymentEntry.query.filter_by(user_id=user_id)
        if payment_category:
            user_payment_entries_query = user_payment_entries_query.filter(PaymentEntry.payment_category == payment_category)
        if month:
            user_payment_entries_query = user_payment_entries_query.filter(db.func.extract('month', PaymentEntry.created_at) == month)    
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
    
