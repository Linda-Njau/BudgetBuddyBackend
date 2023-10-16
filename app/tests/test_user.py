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
    
    def test_update_user(self):
        with self.app.app_context():
            updated_data = {
                'email': 'updateduser@example.com',
                'username': 'updateduser'
            }
        
            response = self.client.put(f'/users/{self.user_id}', json=(updated_data))
            self.assertEqual(response.status_code, 200)
            with db.session() as session:
                updated_user = session.get(User, self.user_id)
                self.assertIsNotNone(updated_user)
                self.assertEqual(updated_user.email, 'updateduser@example.com')
                self.assertEqual(updated_user.username, 'updateduser')
                
    def test_delete_user(self):
        with self.app.app_context():
            response = self.client.delete(f'/users/{self.user_id}')
            self.assertEqual(response.status_code, 200)
            with db.session() as session:
                deleted_user = session.get(User, self.user_id)
                self.assertIsNone(deleted_user)
                response_data = response.get_json()
                self.assertEqual(response_data['message'], 'User deleted successfully')

    def test_patch_user(self):
        with self.app.app_context():
            patch_data = {
                "username": "patchuser",
                "email": "patchuser@example.com"
            }
            response = self.client.patch(f'/users/{self.user_id}', json=patch_data)
            self.assertEqual(response.status_code, 200)
            with db.session() as session:
                patched_user = session.get(User, self.user_id)
                self.assertEqual(patched_user.user_id, self.user_id)
                self.assertEqual(patched_user.username, "patchuser")
                self.assertEqual(patched_user.password_hash, "testpassword")
                self.assertEqual(patched_user.email, "patchuser@example.com")
    
    
    def test_get_payment_entries(self):
        with self.app.app_context():
            user_id = self.test_user.user_id
            payment_entry1 = PaymentEntry(
                amount=50,
                transaction_date=date(2023, 1, 10),
                payment_category=PaymentCategory.FOOD,
                created_at=datetime(2023, 1, 15),
                updated_at=datetime(2023, 1, 15),
                
                user_id=self.test_user.user_id
            )
            payment_entry2 = PaymentEntry(
                amount=75,
                transaction_date =date(2023, 2, 10),
                payment_category=PaymentCategory.TRAVEL,
                created_at=datetime(2023, 2, 20),
                updated_at =datetime(2023, 2, 20),
                user_id=user_id
            )
            payment_entry3 = PaymentEntry(
                amount=100,
                transaction_date =date(2023, 1, 10),
                payment_category=PaymentCategory.FOOD,
                created_at=datetime(2023, 1, 20),
                updated_at=datetime(2023, 1, 20),
                user_id=user_id
            )
            db.session.add(payment_entry1)
            db.session.add(payment_entry2)
            db.session.add(payment_entry3)
            db.session.commit()
            
            response = self.client.get(f'/users/{user_id}/payment_entries')
            self.assertEqual(response.status_code, 200)
            response_data = response.get_json()
            print(response_data)
            self.assertEqual(len(response_data), 3)
            
            for payment_entry in response_data:
                self.assertIn('payment_category', payment_entry)
                
            response = self.client.get(f'/users/{user_id}/payment_entries?payment_category=FOOD')
            print("URL:", f'/users/{user_id}/payment_entries?payment_category=FOOD')
            self.assertEqual(response.status_code, 200)
            response_data = response.get_json()
            print("Response Data:", response_data)
            self.assertEqual(len(response_data), 2)
            self.assertEqual(response_data[0]['payment_category'], PaymentCategory.FOOD.value)
            
            response = self.client.get(f'/users/{user_id}/payment_entries?payment_category=TRAVEL')
            print("URL:", f'/users/{user_id}/payment_entries?payment_category=TRAVEL')
            self.assertEqual(response.status_code, 200)
            response_data = response.get_json()
            print("Response Data:", response_data)
            self.assertEqual(len(response_data), 1)
            self.assertEqual(response_data[0]['payment_category'], PaymentCategory.TRAVEL.value)
            
            response = self.client.get(f'/users/{user_id}/payment_entries?month=1')
            self.assertEqual(response.status_code, 200)
            response_data = response.get_json()
            print("URL:", f'/users/{user_id}/payment_entries?month=1/')
            print("Response Data:", response_data)
            self.assertEqual(len(response_data), 2)
            
            response = self.client.get(f'/users/{user_id}/payment_entries?payment_category=FOOD&month=1')
            self.assertEqual(response.status_code, 200)
            print("URL:", f'/users/{user_id}/payment_entries?payment_category=FOOD&month=1')
            response_data = response.get_json()
            print("Response Data:", response_data)
            self.assertEqual(len(response_data), 2)
