import unittest
from datetime import datetime
from unittest.mock import patch
from email_service import EmailService
from main import OverSpending
from app.api.services.payment_entry_service import PaymentEntryService
from app.models import PaymentCategory
from email_service import EmailService

class MockEmailService(EmailService):
    def send_email(self, from_email, to_email, subject, content):
        # Actual implementation of email sending
        return True
    
class MockPaymentEntryService(PaymentEntryService):
     def get_payment_entries(self, user_id, payment_category=None, month=None):
        now = datetime.utcnow()
        current_month = now.month
        previous_month = current_month -1
        data = {
            "42": {
                current_month : {"payment_category": PaymentCategory.FOOD.value, "amount": 10000},
                previous_month : {"payment_category": PaymentCategory.FOOD.value, "amount": 4000},
                },
            "21": {
                current_month: {"payment_category": PaymentCategory.FOOD.value, "amount": 10000},
                previous_month: {"payment_category": PaymentCategory.FOOD.value, "amount": 11000},
            },
            "56": {
                current_month: {"payment_category": PaymentCategory.FOOD.value, "amount": 15000},
                previous_month: {"payment_category": PaymentCategory.FOOD.value, "amount": 10000},
            },
        }
        return [
            {"payment_category": data[user_id][month]["payment_category"], "amount": data[user_id][month]["amount"]}
        ]
    
mock_payment_entry_service = MockPaymentEntryService()
mock_email_service = MockEmailService()
over_spending = OverSpending(mock_payment_entry_service, mock_email_service)


class TestUnusualSpending(unittest.TestCase):
    @patch.object(EmailService, 'send_email', autospec=True)        
    def test_with_overspending(self, mock_send_email): 
        result = over_spending.is_over_spending("42", payment_category=PaymentCategory.FOOD, month=datetime.utcnow().month)
        mock_send_email.assert_called_once()
        self.assertTrue(result)
    
    
    @patch.object(MockEmailService, 'email')      
    def test_over_spending_without_overspending(self, mock_send_email):        
        result = over_spending.is_over_spending(self, mock_send_email)
        mock_send_email.assert_not_called()
        self.assertFalse(result)

    @patch.object(MockEmailService, 'email', autospec=True)
    def test_over_spending_with_multiple_categories(self, mock_send_email):
        result = over_spending.is_over_spending("42", payment_category=None, month=datetime.utcnow().month)
        mock_send_email.assert_called_once()
        self.assertTrue(result)
       
    @patch.object(MockEmailService, 'email', autospec=True)
    def test_over_spending_with_overspending_in_both_categories(self, mock_send_email):
        result = over_spending.is_over_spending("56", payment_category=None, month=datetime.utcnow().month)
        mock_send_email.assert_called_once()  # Assert that email is sent
        self.assertTrue(result)
