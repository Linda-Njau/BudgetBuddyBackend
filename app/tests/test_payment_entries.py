import unittest
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
                'transaction_date': '2023-1-10',
                'payment_category': PaymentCategory.FOOD.value,
                'user_id': self.user_id
            }
            print(f"transaction_date type: {type(payment_entry_data['transaction_date'])}")
            response = self.client.post('/payment_entries', json=payment_entry_data)
            self.assertEqual(response.status_code, 201)
            response_data = response.get_json()
            print(f'Here is the response_data{response_data}')
            payment_entry_id = response_data[0].get('payment_entry_id')
            print(response.status_code)
            print(response.get_json())
            self.assertIsNotNone(payment_entry_id)
            with db.session() as session:
                created_payment_entry = session.get(PaymentEntry, self.test_payment_entry_id)
                self.assertEqual(created_payment_entry.amount, 50)
                self.assertEqual(created_payment_entry.payment_category, PaymentCategory.FOOD)
                self.assertEqual(created_payment_entry.user_id, self.user_id)
    
    def test_get_payment_entry(self):
        url = f'/payment_entries/{self.test_payment_entry_id}'
        print(f"Testing URL: {url}")
        response = self.client.get(f'/payment_entries/{self.test_payment_entry_id}')
        self.assertEqual(response.status_code, 200)
        expected_payment_data = {
            "amount": 50.0,
            "transaction_date": "2023-01-10",
            "payment_category": PaymentCategory.FOOD.value
        }
        print("Response Data:", response.get_json())
        print("Expected Payment Data:", expected_payment_data)
        response_data = response.getpayment_category
        self.assertEqual(response_data, expected_payment_data)

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
                self.assertEqual(updated_payment_entry.transaction_date, "2023-01-11")
                self.assertEqual(updated_payment_entry.payment_category, PaymentCategory.TRAVEL)
                