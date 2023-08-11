from app.models import User, PaymentCategory
from app import db


class UserService:
    """Service for interacting with the users endpoints."""
    
    def create_user(self, data):
        """Creates new user"""
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        
        if not email or not password or not username:
            return {'error': 'missing required fields'}, 400
        
        new_user = User(
            email=email,
            username=username,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        
        return {'message' : "Successfully created"}, 201
        
    def get_user(self, user_id):
        """Returns user information by user_id"""
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        user_data = {
            'id' : user.id,
            'email' : user.email,
            'username' : user.username
        }
        return user_data

    def update_user(self, user_id, data):
        """update users by user_id"""
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        
        user.email = email
        user.password = password
        user.username = username
         
        db.session.commit()
        return {'message' : 'User updated successfully'}
    
    def delete_user(self, user_id):
        """Delete a user by id."""
        user = User.query.get(user_id)
        if not user:
            return {'error' : 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        
        return {'message': 'User deleted successfully'}
    
    def create_payment_category(self, user_id, data):
        """needs authentication to be properly implemented"""
        category_name = data.get('category_name')
        
        if not category_name:
            return {'error': 'missing category name'}, 400
        new_payment_category = PaymentCategory(
            category_name = category_name,
            user_id = user_id
        )
        db.session.add(new_payment_category)
        db.session.commit()
        
    def get_payment_categories(self, user_id):
        payment_categories = PaymentCategory.query.filter_by(user_id =user_id).all()
        payment_categories_list = []
        for payment_category in payment_categories:
            payment_category_data = {
                'category_name': payment_category.category_name
            }
            payment_categories_list.append(payment_category_data)
            return payment_categories_list
