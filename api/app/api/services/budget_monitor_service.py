"""Budget monitor class

    Handles the detection of overspending and the email notification
"""
import os
from datetime import datetime, timedelta
from flask_api import status
from app.models import PaymentCategory
from app.api.services.payment_entry_service import PaymentEntryService
from app.api.services.user_service import UserService
from app.api.services.email_service import EmailService


from_email = os.environ.get('FROM_EMAIL_ADDRESS')
class BudgetMonitor:
    """
    Monitors user spending and sends notifications for potential overspending.

    Attributes:
    - payment_entry_service: Service for managing payment entries.
    - email_service: Service for sending emails.
    - user_service: Service for user-related operations.
    """
    
    def __init__(self, payment_entry_service = None, email_service = None, user_service =None):
        """
        Initializes the BudgetMonitor.
        
        Parameters:
        - payment_entry_service: Service for managing payment entries.
        - email_service: Service for sending emails.
        - user_service: Service for user-related operations.
        """
        self.payment_entry_service = payment_entry_service
        self.email_service = email_service
        self.user_service = user_service

    def calculate_total_spending(self, entries_response):
        """
        Calculates the total spending from a list of payment entries.

        Parameters:
          - entries_response: A tuple containing payment entries and a status code.
          
        Returns:
        - Total spending as a float.
        """
        entries, status_code = entries_response
        
        if status_code == status.HTTP_200_OK:
            total_spending = 0
            for entry in entries:
                total_spending += entry["amount"]
            return total_spending
        else:
            return None

    def detect_overspending(self, user_id, payment_category, date_range):
        """
        Checks if the user is overspending in a given payment category for the current month.

        Parameters:
        - user_id: ID of the user.
        - payment_category: Payment category to check for overspending.
        - date_range: Dictionary containing start and end dates for the current and previous months.

        Returns:
        - Tuple: (True if overspending is detected, False otherwise, Percentage of overspending.
        """
        current_month_entries = self.payment_entry_service.get_payment_entries(
        user_id, payment_category, start_date=date_range['current']['start'], end_date=date_range['current']['end']
        )

        previous_month_entries = self.payment_entry_service.get_payment_entries(
        user_id, payment_category, start_date=date_range['previous']['start'], end_date=date_range['previous']['end']
        )

        if not current_month_entries or not previous_month_entries:
            return False, 0.0
        
        current_month_spending = self.calculate_total_spending(current_month_entries)
        previous_month_spending = self.calculate_total_spending(previous_month_entries)
        
        if previous_month_spending == 0:
            return False, 0.0
        
        overspending_detected = current_month_spending >= 1.5 * previous_month_spending
        overspending_percent = ((current_month_spending - previous_month_spending) / previous_month_spending) * 100

        
        if overspending_detected:
            self.notify_overspending(user_id, payment_category, overspending_percent)
        return overspending_detected, overspending_percent
                   
    def notify_overspending(self, user_id, payment_category, overspending_percent):
        """
        Sends an email notification for detected overspending.

        Parameters:
        - user_id: ID of the user.
        - payment_category: Payment category related to overspending.
        - overspending_percent: Percentage of overspending.

        Returns:
        - None
        """
        user_data = self.user_service.get_user(user_id)
        to_email = user_data["email"]
        subject = "Overspending Detected"
        content = f"Overspending detected in the {payment_category} category.\n"
        content += f"You have overspent by {overspending_percent:.2f}% compared to the previous month."
        self.email_service.send_email(to_email, subject, content)



def get_date_ranges():
    """
    Generate date ranges for the current and previous months.

    Returns:
    - Dictionary with start and end dates for the current and previous months.
    """
    today = datetime.today()
    if today.month == 1:
        first_day_prev_month = datetime(today.year -1, 12, 1)
        last_day_prev_month = datetime(today.year -1, 12, 1) - timedelta(days=1)
    else:
        first_day_prev_month = datetime(today.year, today.month - 1, 1)
        last_day_prev_month = datetime(today.year, today.month, 1) - timedelta(days=1)
        
    first_day_current_month = datetime(today.year, today.month, 1)
    last_day_current_month = datetime(today.year, today.month + 1, 1) - timedelta(days=1)   
    date_ranges = {
        'current': {'start': first_day_current_month, 'end': last_day_current_month},
        'previous': {'start': first_day_prev_month, 'end': last_day_prev_month}
        }
    return date_ranges
