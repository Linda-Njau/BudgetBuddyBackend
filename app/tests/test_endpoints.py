import unittest
from .. import create_app
from app.models import User, PaymentCategory, PaymentEntry
from app import db

flask_app = create_app(environment="testing")


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(environment="testing")
        self.client = self.app.test_client()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
    def test_create_user(self):
        user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpassword'
            }
        with self.app.app_context():
            response = self.client.post('/users', json=user_data)
            self.assertEqual(response.status_code, 201)
            
            created_user = User.query.filter_by(username=user_data['username']).first()
            self.assertIsNotNone(created_user)
            self.assertEqual(created_user.email, user_data['email'])
            self.assertIsNotNone(created_user.user_id)

    def test_get_user(self):
        with self.app.app_context():
            test_user = User(
                username='testuser',
                email='testuser@example.com',
                password_hash='testpassword'
                )
            db.session.add(test_user)
            db.session.commit()
            user_id = test_user.user_id
        response = self.client.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        expected_user_data = {
            'user_id': user_id,
            'username': 'testuser',
            'email': 'testuser@example.com'
        }
        response_data = response.get_json()
        self.assertEqual(response_data, expected_user_data)
    
    def test_update_user(self):
        with self.app.app_context():
            test_user = User(
                username='testuser',
                email='testuser@example.com',
                password_hash='testpassword'
            )
            db.session.add(test_user)
            db.session.commit()
            user_id = test_user.user_id
            updated_data = {
                'email': 'updateduser@example.com',
                'username': 'updateduser'
            }
        
            response = self.client.put(f'/users/{user_id}', json=(updated_data))
            self.assertEqual(response.status_code, 200)
            with db.session() as session:
                updated_user = session.get(User, user_id)
                self.assertIsNotNone(updated_user)
                self.assertEqual(updated_user.email, 'updateduser@example.com')
                self.assertEqual(updated_user.username, 'updateduser')
                
    def test_delete_user(self):
        with self.app.app_context():
            test_user = User(
                username='testuser',
                email='testuser@example.com',
                password_hash='testpassword'
            )
            db.session.add(test_user)
            db.session.commit()
            user_id = test_user.user_id
            response = self.client.delete(f'/users/{user_id}')
            self.assertEqual(response.status_code, 200)
            with db.session() as session:
                deleted_user = session.get(User, user_id)
                self.assertIsNone(deleted_user)
                response_data = response.get_json()
                self.assertEqual(response_data['message'], 'User deleted successfully')

    def test_create_payment_entry(self):
        with self.app.app_context():
            test_user = User(
                username='testuser',
                email='testuser@example.com',
                password_hash='testpassword'
            )
            db.session.add(test_user)
            db.session.commit()
            user_id = test_user.user_id
            
            payment_entry_data = {
                'amount': 50,
                'payment_category': PaymentCategory.FOOD.value,
                'user_id': user_id
            }
            response = self.client.post('/payment_entries', json=payment_entry_data)
            self.assertEqual(response.status_code, 201)
            response_data = response.get_json()
            print(f'Here is the response_data{response_data}')
            payment_entry_id = response_data[0].get('payment_entry_id')
            print(response.status_code)
            print(response.get_json())
            self.assertIsNotNone(payment_entry_id)
            created_payment_entry = PaymentEntry.query.get(payment_entry_id)
            self.assertEqual(created_payment_entry.amount, 50)
            self.assertEqual(created_payment_entry.payment_category, PaymentCategory.FOOD)
            self.assertEqual(created_payment_entry.user_id, test_user.user_id)
