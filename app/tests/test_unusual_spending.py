import email
import unittest
from datetime import datetime
from unittest.mock import MagicMock
from app.api.services.email_service import EmailService
from app.api.services.budget_monitor_service import OverSpending
from app.api.services.payment_entry_service import PaymentEntryService
from app.models import PaymentCategory
from app.api.services.email_service import EmailService

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
    
class TestUnusualSpending(unittest.TestCase):
    def setUp(self):
        self.mock_payment_entry_service = MockPaymentEntryService()
        self.mock_email_service = MockEmailService()
        self.email_service_mock = MagicMock()
        self.over_spending = OverSpending(self.mock_payment_entry_service, self.email_service_mock)
        
    def test_with_overspending(self):
        result = self.over_spending.is_over_spending("42", payment_category=PaymentCategory.FOOD, month=datetime.utcnow().month)
        self.email_service_mock.send_email.assert_called_once()
        self.assertTrue(result)

    def test_without_overspending(self):
        result = self.over_spending.is_over_spending("21", payment_category=PaymentCategory.FOOD, month=datetime.utcnow().month)
        self.email_service_mock.send_email.assert_not_called()
        self.assertFalse(result)

    def test_over_spending_with_multiple_categories(self):
        result = self.over_spending.is_over_spending("42", payment_category=None, month=datetime.utcnow().month)
        self.email_service_mock.send_email.assert_called_once()
        self.assertTrue(result)

    def test_with_overspending_in_both_categories(self):
        result = self.over_spending.is_over_spending("56", payment_category=None, month=datetime.utcnow().month)
        self.email_service_mock.send_email.assert_called_once()
        self.assertTrue(result)
