from app.models import User
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
