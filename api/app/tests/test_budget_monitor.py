from app.api.services.budget_monitor_service import BudgetMonitor
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

class TestBudgetMonitor(unittest.TestCase):

    def setUp(self):
        self.payment_entry_service = MagicMock()
        self.email_service = MagicMock()
        self.user_service = MagicMock()

    
        self.budget_monitor = BudgetMonitor(
            payment_entry_service=self.payment_entry_service,
            email_service=self.email_service,
            user_service=self.user_service
        )

    def test_detect_overspending_false(self):
        self.payment_entry_service.get_payment_entries.side_effect = [
            [
                {'id': 46, 'amount': 600.0, 'transaction_date': '2023-06-15', 'payment_category': 'FOOD'},
                {'id': 48, 'amount': 400.0, 'transaction_date': '2023-06-10', 'payment_category': 'FOOD'},
            ],
            [
                {'id': 47, 'amount': 800.0, 'transaction_date': '2023-05-20', 'payment_category': 'FOOD'},
                {'id': 49, 'amount': 700.0, 'transaction_date': '2023-05-10', 'payment_category': 'FOOD'},
            ],
    ]

        self.user_service.get_user.return_value = {"email": "test@example.com"}
        
        today = datetime(2023, 6, 15)
        date_ranges = {
            'current': {'start': datetime(today.year, today.month, 1), 'end': datetime(today.year, today.month + 1, 1) - timedelta(days=1)},
            'previous': {'start': datetime(today.year, today.month - 1, 1),
                         'end': datetime(today.year, today.month, 1) - timedelta(days=1)}
        }
   
        overspending_detected, overspending_percent = self.budget_monitor.detect_overspending(
            user_id=1, payment_category="FOOD", date_range=date_ranges
        )


        self.assertFalse(overspending_detected)
        self.assertEqual(overspending_percent, 0.0)
        self.email_service.send_email.assert_not_called()

    def test_detect_overspending_true(self):
        self.payment_entry_service.get_payment_entries.side_effect =[
            [
                {'id': 46, 'amount': 700.0, 'transaction_date': '2023-06-15', 'payment_category': 'FOOD'},
                {'id': 48, 'amount': 800.0, 'transaction_date': '2023-06-10', 'payment_category': 'FOOD'},
            ],
            [
                {'id': 47, 'amount': 500.0, 'transaction_date': '2023-05-20', 'payment_category': 'FOOD'},
                {'id': 49, 'amount': 500.0, 'transaction_date': '2023-05-10', 'payment_category': 'FOOD'},
            ],
    ]
        self.user_service.get_user.return_value = {"email": "test@example.com"}

        today = datetime(2023, 6, 15)
        date_ranges = {
            'current': {'start': datetime(today.year, today.month, 1), 'end': today},
            'previous': {'start': datetime(today.year, today.month - 1, 1),
                         'end': datetime(today.year, today.month, 1) - timedelta(days=1)}
        }

        overspending_detected, overspending_percent = self.budget_monitor.detect_overspending(
            user_id=1, payment_category="FOOD", date_range=date_ranges
        )
        
        self.assertTrue(overspending_detected)
        self.assertEqual(overspending_percent, 50.0)
        self.email_service.send_email.assert_called_once_with(
            "test@example.com", "Overspending Detected",
            "Overspending detected in the FOOD category.\n"
            "You have overspent by 50.00% compared to the previous month."
        )

if __name__ == '__main__':
    unittest.main()
