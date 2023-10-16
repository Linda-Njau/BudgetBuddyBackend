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
        
            return {'message' : "Successfully created"}, 201
        except Exception as error:
            db.session.rollback()
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
    
    def get_all_users(self):
        """Returns all user information"""
        with db.session() as session:
            users = session.query(User).all()
            if not users:
                return {'error': 'No users were found'}, 404
            
            users_data = []
            for user in users:
                user_data = {
                    'user_id': user.user_id,
                    'email': user.email,
                    'username': user.username,
                }
                users_data.append(user_data)
            return users_data

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
    
    def patch_user(self, user_id, data):
        with db.session() as session:
            user = session.get(User, user_id)
            if not user:
                return{"error": "User not found"}, 404
            if 'email' in data:
                user.email = (data['email'])
            if 'password' in data:
                user.password = (data['password'])
            if 'username' in data:
                user.username = (data['username'])
            db.session.commit()
            return {"message": "User updated successfully"}, 200
    
    def delete_user(self, user_id):
        """Delete a user by id."""
        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
            return {'error' : 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        
        return {'message': 'User deleted successfully'}

    