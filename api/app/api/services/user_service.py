from werkzeug.security import generate_password_hash
import re
from ...models import User, PaymentCategory, PaymentEntry
from ... import db
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

def get_success_message(data, status_code=status.HTTP_200_OK):
    """
    Create a standardized success response.

    Args:
        data (dict): The data to be included in the success response.
        status_code (int, optional): The HTTP status code. Defaults to 200 OK.

    Returns:
        dict: A dictionary containing the data and a success message, along with the status code.
    """
    return {'data': data, 'message': 'success'}, status_code

class UserService:
    """Service for interacting with the users endpoints."""
    
    def is_valid_user(self, data, context):
        error_messages = []
        if context == 'create' or context == 'update':
            if 'email' not in data:
                error_messages.append("Please provide an email address")
            else:
                if not self.is_valid_format(data['email']):
                    error_messages.append("Invalid email format")
                if context == 'create' and self.is_email_taken(data['email']):
                    error_messages.append("Email address already in use")
                if context == 'create' and self.is_username_taken(data['username']):
                    error_messages.append("Username already in use")
                    
            if 'password' not in data:
                error_messages.append("Please provide a password")
            elif len(data['password']) < 8:
                error_messages.append("Password must be at least 8 characters long")
            
            if 'username' not in data:
                error_messages.append("Please provide a username")
            elif len(data['username']) < 3:
                error_messages.append("Username must be at least 3 characters long")
        
        if error_messages:
            print("Validation failed. Errors:", error_messages)
            return False, error_messages
        return True, None
    
    def is_username_taken(self, username):
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"Username '{username}' already in use.")
        return existing_user is not None

    def is_valid_format(self, email):
        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return re.match(email_regex, email) is not None
    
    def is_email_taken(self, email):
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"email '{email}' already in use")
        return existing_user is not None
    
    def create_user(self, data, context='create'):
        """Creates new user"""
        is_valid, errors = self.is_valid_user(data, context)
        
        if not is_valid:
            return get_error_message(errors, 400)
        
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
        
        db.session.add(new_user)
        db.session.commit()
        
        return get_success_message({'user_id': new_user.user_id}), 201
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

    