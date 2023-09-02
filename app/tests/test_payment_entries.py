import unittest
from .. import create_app
from app import db
from app.models import User, PaymentEntry, PaymentCategory
from datetime import datetime


class TestPaymentEntriesEndpints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(environment="testing")
        self.client = self.app.test_client()
        
        with self.app.app_context():
            self.test_user = User(
                username="test_user",
                email="testuser@example.com",
                password_hash = "testpassword"
            )
            db.session.add(self.test_user)
            db.session.commit()
            self.user_id = self.test_user.user_id
            
            self.test_payment_entry = PaymentEntry(
                amount=50,
                payment_category=PaymentCategory.FOOD,
                created_at=datetime(2023, 1, 15),
                user_id=self.user_id
            )
            db.session.add(self.test_payment_entry)
            db.session.commit()
            self.test_payment_entry_id = self.test_payment_entry.id 

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
            
    def test_create_payment_entry(self):
        with self.app.app_context():
            payment_entry_data = {
                'amount': 50,
                'payment_category': PaymentCategory.FOOD.value,
                'user_id': self.user_id
            }
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
            "amount" : 50,
            "payment_category" : PaymentCategory.FOOD,
            "created_at" : datetime(2023, 1, 15),
            "user_id" : self.user_id
        }
        response_data = response.get_json()
        self.assertEqual(response_data, expected_payment_data)
