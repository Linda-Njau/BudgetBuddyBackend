import unittest
from app import create_app
from app.models import User, PaymentCategory, PaymentEntry
from app import db
from datetime import datetime, date

flask_app = create_app(environment="testing")


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(environment="testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.test_user = User(
                username="test_user1",
                email="testuser1@example.com",
                password_hash = "testpassword"
            )
            db.session.add(self.test_user)
            db.session.commit()
            self.user_id = self.test_user.user_id
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.session.commit()
            db.drop_all()
            
    def test_create_user(self):
        user_data = {
            'email': 'testuser2@example.com',
            'username': 'testuser2',
            'password': 'testpassword'
            }
        response = self.client.post('/users', json=user_data)
        self.assertEqual(response.status_code, 201)
        with self.app.app_context():
            with self.app.test_request_context():
                created_user = User.query.filter_by(username=user_data['username']).first()
                self.assertIsNotNone(created_user)
                self.assertEqual(created_user.email, user_data['email'])
                self.assertIsNotNone(created_user.user_id)

    def test_create_user_invalid_data(self):
        invalid_data = {
            'email': 'email',
            'username': '1',
            'password': '1'
        }
        response = self.client.post('/users', json=(invalid_data))
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        expected_error_message = {'error': 'Invalid email format; Password must be at least 8 characters long; Username must be at least 3 characters long'}
        self.assertEqual(response_data, expected_error_message)
    
    def test_create_user_missing_data(self):
        missing_data = {}
        response = self.client.post('/users', json=(missing_data))
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        expected_error_message = {'error': 'Please provide an email address; Please provide a password; Please provide a username'}
        self.assertEqual(response_data, expected_error_message)
           
        
    def test_get_user(self):
        response = self.client.get(f'/users/{self.user_id}')
        self.assertEqual(response.status_code, 200)
        expected_user_data = {
            'user_id': self.user_id,
            'username': 'test_user1',
            'email': 'testuser1@example.com'
        }
        response_data = response.get_json()
        self.assertEqual(response_data, expected_user_data)
    
    def test_get_user_invalid_id(self):    
        response = self.client.get(f'/users/{1234}')
        self.assertEqual(response.status_code, 404)
        response_data = response.get_json()
        expected_error_message = {'error': 'User not found'}
        self.assertEqual(response_data, expected_error_message)
    
    def test_update_user(self):
        with self.app.app_context():
            updated_data = {
                'email': 'updateduser@example.com',
                'username': 'updateduser'
            }
        
            response = self.client.patch(f'/users/{self.user_id}', json=(updated_data))
            self.assertEqual(response.status_code, 200)
            with db.session() as session:
                updated_user = session.get(User, self.user_id)
                self.assertIsNotNone(updated_user)
                self.assertEqual(updated_user.email, 'updateduser@example.com')
                self.assertEqual(updated_user.username, 'updateduser')
     
    def test_update_user_invalid_data(self):
         with self.app.app_context():
            invalid_data = {
                'email': 'email',
                'username': '1',
                'password': '1'
            }
            response = self.client.patch(f'/users/{self.user_id}', json=(invalid_data))
            self.assertEqual(response.status_code, 400)
            response_data = response.get_json()
            expected_error_messages = {'error': 'Invalid email format; Password must be at least 8 characters long; Username must be at least 3 characters long'}
            self.assertEqual(response_data, expected_error_messages)
              
             
    def test_update_user_invalid_id(self):
        with self.app.app_context():
            updated_data = {
                'email': 'updateduser@example.com',
                'username': 'updateduser'
            }
        
            response = self.client.patch(f'/users/{1234}', json=(updated_data))
            self.assertEqual(response.status_code, 404)
            response_data = response.get_json()
            expected_error_message = {'error': 'User not found'}
            self.assertEqual(response_data, expected_error_message)
                       
    def test_delete_user(self):
        with self.app.app_context():
            response = self.client.delete(f'/users/{self.user_id}')
            self.assertEqual(response.status_code, 202)
            with db.session() as session:
                deleted_user = session.get(User, self.user_id)
                self.assertIsNone(deleted_user)
    
    def test_delete_user_invalid_id(self):
        response = self.client.delete(f'users/{1234}')
        self.assertEqual(response.status_code, 404)
        response_data = response.get_json()
        expected_error_message = {'error': 'User not found'}
        self.assertEqual(response_data, expected_error_message)
                           
    
    