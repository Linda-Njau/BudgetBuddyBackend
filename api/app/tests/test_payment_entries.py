import unittest

from app.api.payment_entry import delete_payment_entry
from .. import create_app
from app import db
from app.models import User, PaymentEntry, PaymentCategory
from datetime import datetime, date


class TestPaymentEntriesEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(environment="testing")
        self.client = self.app.test_client()
        
        with self.app.app_context():
            self.test_user = User(
                username="test_user5",
                email="testuser5@example.com",
                password_hash = "testpassword"
            )
            db.session.add(self.test_user)
            db.session.commit()
            self.user_id = self.test_user.user_id
            
            self.test_payment_entry = PaymentEntry(
                amount=50.0,
                transaction_date=date(2023, 1, 10),
                payment_category=PaymentCategory.FOOD,
                user_id=self.user_id
            )
            db.session.add(self.test_payment_entry)
            db.session.commit()
            self.test_payment_entry_id = self.test_payment_entry.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.session.commit()
            db.drop_all()
            
            
    def test_create_payment_entry(self):
        with self.app.app_context():
            payment_entry_data = {
                'amount': 50,
                'transaction_date': '2023-01-10',
                'payment_category': PaymentCategory.FOOD.value,
                'user_id': self.user_id
            }
            response= self.client.post('/payment_entries', json=payment_entry_data)
            self.assertEqual(response.status_code, 201)
            response_data = response.get_json()
            print(response_data)
            payment_entry_id = response_data.get('payment_entry_id')
            self.assertIsNotNone(payment_entry_id)
            with db.session() as session:
                created_payment_entry = session.get(PaymentEntry, self.test_payment_entry_id)
                self.assertEqual(created_payment_entry.amount, 50)
                self.assertEqual(created_payment_entry.payment_category, PaymentCategory.FOOD)
                self.assertEqual(created_payment_entry.user_id, self.user_id)
    
    def test_create_payment_entry_invalid_data(self):
        with self.app.app_context():
            invalid_data = {
                'amount': -50,
                'transaction_date': 'Monday',
                'payment_category': 'SPORTS',
                'user_id': self.user_id
            }
            response= self.client.post('/payment_entries', json=invalid_data)
            self.assertEqual(response.status_code, 400)
            response_data = response.get_json()
            print(response_data)
            expected_error_message = {'error': 'Amount must be positive number.; Invalid payment category; Invalid transaction date format. Use YYYY-MM-DD'}
            self.assertEqual(response_data, expected_error_message)
        
    def test_create_payment_entry_invalid_user(self):
        with self.app.app_context():
            payment_entry_data = {
                'amount': 50,
                'transaction_date': '2023-01-10',
                'payment_category': PaymentCategory.FOOD.value,
                'user_id': "invalid_user_id"
            }
            response= self.client.post('/payment_entries', json=payment_entry_data)
            self.assertEqual(response.status_code, 404)
            response_data = response.get_json()
            print(response_data)
            expected_error_message ={'error': 'User not found'}
            self.assertEqual(response_data, expected_error_message)
    
    def test_create_payment_entry_missing_data(self):
        with self.app.app_context():
            missing_data = {
                'user_id': self.user_id
            }
            response = self.client.post('/payment_entries', json=(missing_data))
            self.assertEqual(response.status_code, 400)
            response_data = response.get_json()
            expected_error_message = {'error': 'Please provide a valid amount; Please provide a payment category; Please provide a transaction date'}
            self.assertEqual(response_data, expected_error_message)
        
    def test_get_payment_entry(self):
        response = self.client.get(f'/payment_entries/{self.test_payment_entry_id}')
        self.assertEqual(response.status_code, 200)
        expected_payment_data = {
            "amount": 50.0,
            "transaction_date": "2023-01-10",
            "payment_category": PaymentCategory.FOOD.value
        }
        response_data = response.get_json()
        self.assertEqual(response_data, expected_payment_data)

    def test_get_payment_entry_invalid_id(self):
        response = self.client.get(f'payment_entries/{12345}')
        self.assertEqual(response.status_code, 404)
        response_data = response.get_json()
        expected_error_message = {'error': 'Payment entry not found'}
        self.assertEqual(response_data, expected_error_message)
        
        
    def test_update_payment_entry(self):
        with self.app.app_context():
            update_data = {
                "amount": 75.0,
                "transaction_date" : "2023-01-11",
                "payment_category": PaymentCategory.TRAVEL.value
            }
            response = self.client.put(f'/payment_entries/{self.test_payment_entry_id}', json=(update_data))
            self.assertEqual(response.status_code, 200)
            with db.session() as session:
                updated_payment_entry = session.get(PaymentEntry, self.test_payment_entry_id)
                self.assertEqual(updated_payment_entry.user_id, self.user_id)
                self.assertEqual(updated_payment_entry.amount, 75.0)
                expected_transaction_date = datetime.strptime("2023-01-11", '%Y-%m-%d').date()
                self.assertEqual(updated_payment_entry.transaction_date, expected_transaction_date)
                self.assertEqual(updated_payment_entry.payment_category, PaymentCategory.TRAVEL)
    
    def test_update_payment_entry_missing_data(self):
        with self.app.app_context():
            missing_update_data = {}
            response = self.client.put(f'/payment_entries/{self.test_payment_entry_id}', json=(missing_update_data))
            self.assertEqual(response.status_code, 400)
            response_data = response.get_json()
            expected_error_message = {'error': 'Please provide a valid amount; Please provide a payment category; Please provide a transaction date'}
            self.assertEqual(response_data, expected_error_message)
            
    def test_update_payment_entry_invalid_data(self):
        with self.app.app_context():
            invalid_data = {
                'amount': '0.00',
                'transaction_date': '2023 Monday May',
                'Payment_category': 'sports'
            }
            response = self.client.put(f'/payment_entries/{self.test_payment_entry_id}', json=(invalid_data))
            self.assertEqual(response.status_code, 400)
            response_data = response.get_json()
            expected_error_message = {'error': 'Amount must be positive number.; Please provide a payment category; Invalid transaction date format. Use YYYY-MM-DD'}
            self.assertEqual(response_data, expected_error_message)
    
    def test_update_payment_entry_invalid_id(self):
         with self.app.app_context():
            update_data = {
                "amount": 75.0,
                "transaction_date" : "2023-01-11",
                "payment_category": PaymentCategory.TRAVEL.value
            }
            response = self.client.put(f'payment_entries/{12345}', json=(update_data))
            self.assertEqual(response.status_code, 404)
            response_data = response.get_json()
            expected_error_message = {'error': 'Payment entry not found'}
            self.assertEqual(response_data, expected_error_message)    
        
    def test_patch_payment_entry(self):
        with self.app.app_context():
            patch_data = {
                "payment_category": PaymentCategory.TRAVEL.value,
                "transaction_date": "2023-01-11" 
            }
            response = self.client.patch(f'/payment_entries/{self.test_payment_entry_id}', json=(patch_data))
            self.assertEqual(response.status_code, 200)
            with db.session() as session:
                patched_payment_entry = session.get(PaymentEntry, self.test_payment_entry_id)
                self.assertEqual(patched_payment_entry.amount, 50.0)
                expected_transaction_date = datetime.strptime("2023-01-11", '%Y-%m-%d').date()
                self.assertEqual(patched_payment_entry.transaction_date, expected_transaction_date)
                self.assertEqual(patched_payment_entry.payment_category, PaymentCategory.TRAVEL)
                
    def test_patch_payment_entry_invalid_data(self):
        with self.app.app_context():
            invalid_data = {
                'amount': '0.00',
                'transaction_date': '2023 Monday May',
                'payment_category': 'sports'
            }
            response = self.client.patch(f'/payment_entries/{self.test_payment_entry_id}', json=(invalid_data))
            self.assertEqual(response.status_code, 400)
            response_data = response.get_json()
            print(response_data)
            expected_error_message = {'error': 'Amount must be positive number.; Invalid payment category; Invalid transaction date format. Use YYYY-MM-DD'}
            self.assertEqual(response_data, expected_error_message)
            
    def test_patch_payment_entry_invalid_id(self):
         with self.app.app_context():
            patch_data = {
                "amount": 75.0,
                "transaction_date" : "2023-01-11",
                "payment_category": PaymentCategory.TRAVEL.value
            }
            response = self.client.patch(f'payment_entries/{12345}', json=(patch_data))
            self.assertEqual(response.status_code, 404)
            response_data = response.get_json()
            expected_error_message = {'error': 'Payment entry not found'}
            self.assertEqual(response_data, expected_error_message)
            
    def test_delete_payment_entry(self):
        with self.app.app_context():
            response = self.client.delete(f'/payment_entries/{self.test_payment_entry_id}')
            self.assertEqual(response.status_code, 204)
            with db.session() as session:
                deleted_payment_entry = session.get(PaymentEntry, self.test_payment_entry_id)
                self.assertIsNone(deleted_payment_entry)

    def test_delete_payment_entry_invalid_id(self):
         with self.app.app_context():
            response = self.client.delete(f'payment_entries/{12345}')
            self.assertEqual(response.status_code, 404)
            response_data = response.get_json()
            expected_error_message = {'error': 'Payment entry not found'}
            self.assertEqual(response_data, expected_error_message)
            
    def test_get_payment_entries(self):
        with self.app.app_context():
            db.session.add(self.test_user)
            db.session.flush()
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
            self.assertEqual(len(response_data), 4)
            
            for payment_entry in response_data:
                self.assertIn('payment_category', payment_entry)
                
            response = self.client.get(f'/users/{user_id}/payment_entries?payment_category=FOOD')
            self.assertEqual(response.status_code, 200)
            response_data = response.get_json()
            self.assertEqual(len(response_data), 3)
            self.assertEqual(response_data[0]['payment_category'], PaymentCategory.FOOD.value)
            
            response = self.client.get(f'/users/{user_id}/payment_entries?payment_category=TRAVEL')
            self.assertEqual(response.status_code, 200)
            response_data = response.get_json()
            self.assertEqual(len(response_data), 1)
            self.assertEqual(response_data[0]['payment_category'], PaymentCategory.TRAVEL.value)
            
            response = self.client.get(f'/users/{user_id}/payment_entries?month=1')
            self.assertEqual(response.status_code, 200)
            response_data = response.get_json()
            print(response_data)
            self.assertEqual(len(response_data), 3)
            
            response = self.client.get(f'/users/{user_id}/payment_entries?payment_category=FOOD&month=1')
            self.assertEqual(response.status_code, 200)
            response_data = response.get_json()
            self.assertEqual(len(response_data), 3)
            
    def test_get_payment_entries_invalid_user_id(self):
            response = self.client.get(f'/users/{1234}/payment_entries')
            self.assertEqual(response.status_code, 404)
            response_data = response.get_json()
            expected_error_message = {'error': 'User not found'}
            self.assertEqual(response_data, expected_error_message)
        
    def test_get_payment_entries_none(self):
         with self.app.app_context():
            self.test_user = User(
                username="test_no_entries",
                email="testnoentries@example.com",
                password_hash = "testpassword"
            )
            db.session.add(self.test_user)
            db.session.commit()
            self.user_id = self.test_user.user_id
            
            response = self.client.get(f'/users/{self.test_user.user_id}/payment_entries')
            self.assertEqual(response.status_code, 404)
            response_data = response.get_json()
            expected_error_message = {'error': 'No payment entries for this user'}
            self.assertEqual(response_data, expected_error_message)
            