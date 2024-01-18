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

def get_success_message(data=None):
    """
    Create a standardized success response.

    Args:
        data (dict): The data to be included in the success response.
        status_code (int, optional): The HTTP status code. Defaults to 200 OK.

    Returns:
        dict: A dictionary containing the data and a success message, along with the status code.
    """
    return {'data': data, 'message': 'success'}

class UserService:
    """Service for interacting with the users endpoints."""
    
    def is_valid_user(self, data, context):
        """
    Validates user data based on the specified context ('create' or 'update').

    Args:
        data (dict): The data dictionary containing user information.
        context (str): The context in which the validation is being performed ('create' or 'update').

    Returns:
        tuple: A tuple containing a boolean indicating validity and a list of error messages, if any.
    """
        error_messages = []
        if context == 'create':
            if 'email' not in data:
                error_messages.append("Please provide an email address")
            else:
                if not self.is_valid_format(data['email']):
                    error_messages.append("Invalid email format")
                if self.is_email_taken(data['email']):
                    error_messages.append("Email address already in use")
                
                    
            if 'password' not in data:
                error_messages.append("Please provide a password")
            elif len(data['password']) < 8:
                error_messages.append("Password must be at least 8 characters long")
            
            if 'username' not in data:
                error_messages.append("Please provide a username")
            else:
                if self.is_username_taken(data['username']):
                    error_messages.append("Username already in use")
                if len(data['username']) < 3:
                    error_messages.append("Username must be at least 3 characters long")
        if context == "update":
            if 'email' in data:
                if not self.is_valid_format(data['email']):
                    error_messages.append("Invalid email format")
                if self.is_email_taken(data['email']):
                    error_messages.append("Email address already in use")
            if 'password' in data:
                if len(data['password']) < 8:
                    error_messages.append("Password must be at least 8 characters long")
            if 'username' in data:
                if self.is_username_taken(data['username']):
                    error_messages.append("Username already in use")
                if len(data['username']) < 3:
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
    
    def create_user(self, data):
        """
    Creates a new user based on the provided data.

    Args:
        data (dict): The data dictionary containing user information.
        context (str, optional): The context in which the creation is being performed ('create' by default).

    Returns:
        tuple: A tuple containing a response message and HTTP status code.
    """
        is_valid, errors = self.is_valid_user(data, context="create")
        
        if not is_valid:
            return get_error_message(errors, 400)
        
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        password_hash = generate_password_hash(password)
        
        new_user = User(
            email=email,
            username=username,
            password_hash=password_hash
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        if new_user.user_id:
            return get_success_message({'user_id': new_user.user_id}), status.HTTP_201_CREATED

    def get_user(self, user_id):
        """
        Retrieves user information based on the provided user_id.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            tuple: A tuple containing user information and HTTP status code.
        """
        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
            return get_error_message('User not found', status.HTTP_404_NOT_FOUND)
        
        user_data = {
            'user_id' : user.user_id,
            'email' : user.email,
            'username' : user.username
        }
        return get_success_message(user_data), status.HTTP_200_OK
    
    def get_all_users(self):
        """
    Retrieves information for all users in the system.

    Returns:
        tuple: A tuple containing user information and HTTP status code.
    """
        with db.session() as session:
            users = session.query(User).all()
            if not users:
                return get_error_message('No users were found', status.HTTP_404_NOT_FOUND)
            
            users_data = []
            for user in users:
                user_data = {
                    'user_id': user.user_id,
                    'email': user.email,
                    'username': user.username,
                }
                users_data.append(user_data)
            return get_success_message(users_data), status.HTTP_200_OK

    def update_user(self, user_id, data):
        """
    Updates user information based on the provided user_id and data.

    Args:
        user_id (int): The unique identifier of the user to be updated.
        data (dict): The data dictionary containing updated user information.

    Returns:
        tuple: A tuple containing the updated user information and HTTP status code.
    """
        with db.session() as session:
            user = session.get(User, user_id)
            if not user:
                return get_error_message('User not found', status.HTTP_404_NOT_FOUND)
            is_valid, error_response = self.is_valid_user(data, context="update")
            if not is_valid:
                return get_error_message(error_response, status.HTTP_400_BAD_REQUEST)
            user.update(
                email=data.get('email'),
                password=data.get('password'),
                username=data.get('username')
            )
            db.session.commit()
            updated_user = user.to_dict()
            return get_success_message(updated_user), status.HTTP_200_OK
    
    def delete_user(self, user_id):
        """
    Deletes a user based on the provided user_id.

    Args:
        user_id (int): The unique identifier of the user to be deleted.

    Returns:
        tuple: A tuple containing a success message and HTTP status code.
    """
        with db.session() as session:
            user = session.get(User, user_id)
        if not user:
            return get_error_message('User not found', status.HTTP_404_NOT_FOUND)
        db.session.delete(user)
        db.session.commit()
        
        return get_success_message(), status.HTTP_202_ACCEPTED

    