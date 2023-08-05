import unittest
from datetime import datetime
from unittest.mock import patch
from notify_card_holder_wrapper import NotifyCardHolderWrapper
from fetch_payments_wrappper import FetchPaymentsWrapper
from main import UnusualSpending
"""test suite for unusual spending"""

class MockEmailApi(object):
    def email(self, recipient, subject, message):
        # Actual implementation of email sending
        return 202
    
class MockFetchPaymentsApi(object):
    
    def __init__(self):
        now = datetime.utcnow()
        current_month = now.month
        previous_month = current_month -1
        self.data = {
            "42": {current_month : {"food" : 10000 }, previous_month : {"food" : 4000 }},
            "21": {current_month : {"food" : 10000}, previous_month : {"food" : 11000 }}
        }
        
    def fetch_payments(self, user_id, month):
        return self.data[user_id][month]
    
mock_email_api = MockEmailApi()
mock_fetch_payments_api = MockFetchPaymentsApi()
notify_card_holder = NotifyCardHolderWrapper(mock_email_api)
fetch_payment = FetchPaymentsWrapper(mock_fetch_payments_api)
unusual_spending = UnusualSpending(fetch_payment, None, notify_card_holder)


class TestUnusualSpending(unittest.TestCase):
    @patch.object(NotifyCardHolderWrapper, 'email', autospec=True)        
    def test_unusual_spending_for_text(self, mock_email): 
        unusual_spending.run("42")
        
        mock_email.assert_called_once_with(notify_card_holder,"42", "high_spending")
        
    
    @patch.object(NotifyCardHolderWrapper, 'email')        
    def test_unusual_spending_without_unusual_spending(self, mock_email):        
        unusual_spending.run("21")
        
        mock_email.assert_not_called()

