import unittest
from unittest.mock import patch
from notify_card_holder import NotifyCardHolder
from fetch_payments import FetchPayments
from main import UnusualSpending
"""test suite for unusual spending"""

class MockEmailApi(object):
    def email(self, recipient, subject, message):
        # Actual implementation of email sending
        return 202
    
class MockFetchPaymentsApi(object):
    
    def __init__(self):
        self.data = {
            "42": {"Food" : {"current_month" : 10000, "previous_month" : 4000 }},
            "21": {"Food" : {"current_month" : 10000, "previous_month" : 11000 }}
        }
        
    def fetch_payments(self, user_id, month, year):
        return self.data[user_id]
    
mock_email_api = MockEmailApi()
mock_fetch_payments_api = MockFetchPaymentsApi()
notify_card_holder = NotifyCardHolder(mock_email_api)
fetch_payment = FetchPayments(mock_fetch_payments_api)
unusual_spending = UnusualSpending(fetch_payment, None, notify_card_holder)


class TestUnusualSpending(unittest.TestCase):
    @patch.object(NotifyCardHolder, 'email', autospec=True)        
    def test_unusual_spending_for_text(self, mock_email): 
        unusual_spending.run("42")
        
        mock_email.assert_called_once_with(notify_card_holder,"42", "high_spending")
        
    
    @patch.object(NotifyCardHolder, 'email', autospec=True)        
    def test_unusual_spending_without_unusual_spending(self, mock_email):        
        unusual_spending.run("21")
        
        mock_email.assert_not_called()
    