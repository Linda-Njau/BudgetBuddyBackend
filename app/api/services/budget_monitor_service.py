"""Budget monitor class

    Handles the detection of overspending and the email notification
"""
import os
from datetime import datetime, timedelta
from app.models import PaymentCategory
from app.api.services.payment_entry_service import PaymentEntryService
from app.api.services.user_service import UserService
from app.api.services.email_service import EmailService

api_key = os.environ.get('SENDGRID_API_KEY')
from_email = os.environ.get('FROM_EMAIL_ADDRESS')
class BudgetMonitor:
    """
    Monitors user spending and sends notifications for potential overspending.

    Attributes:
    - payment_entry_service: Service for managing payment entries.
    - email_service: Service for sending emails.
    - user_service: Service for user-related operations.
    """
    
    def __init__(self, payment_entry_service, email_service, user_service):
        """
        Initializes the BudgetMonitor.
        """
        self.payment_entry_service = payment_entry_service
        self.email_service = email_service
        self.user_service = user_service

    def calculate_total_spending(self, entries):
        """
        Calculates the total spending from a list of payment entries.

        Parameters:
        - entries: List of payment entries.

        Returns:
        - Total spending as a float.
        """
        total_spending = 0
        for entry in entries:
            total_spending += entry["amount"]
        return total_spending

    def is_over_spending(self, user_id, payment_category, date_range):
        """
        Checks if the user is overspending in a given payment category for the current month.

        Parameters:
        - user_id: ID of the user.
        - payment_category: Payment category to check for overspending.
        - date_range: Dictionary containing start and end dates for the current and previous months.

        Returns:
        - True if overspending is detected, False otherwise.
        """
        current_month_entries = self.payment_entry_service.get_payment_entries(
        user_id, payment_category, start_date_str=date_range['current']['start'].strftime('%Y-%m-%d'), end_date_str=date_range['current']['end'].strftime('%Y-%m-%d')
        )

        previous_month_entries = self.payment_entry_service.get_payment_entries(
        user_id, payment_category, start_date_str=date_range['previous']['start'].strftime('%Y-%m-%d'), end_date_str=date_range['previous']['end'].strftime('%Y-%m-%d')
        )
        
        if not current_month_entries or not previous_month_entries:
            return False

        current_month_spending = self.calculate_total_spending(current_month_entries)
        previous_month_spending = self.calculate_total_spending(previous_month_entries)
        
        if current_month_spending >= 1.5 * previous_month_spending:
            user_data = self.user_service.get_user(user_id)
            user_email = user_data["email"]
            overspending_percent = ((current_month_spending - previous_month_spending) / previous_month_spending) * 100
            self.send_overspending_email(user_email, payment_category, overspending_percent)
            return True
        else:
            return False

    def send_overspending_email(self, to_email, payment_category, overspending_percent):
        """
        Sends an email notification for detected overspending.

        Parameters:
        - to_email: Email address to send the notification.
        - payment_category: Payment category related to overspending.
        - overspending_percent: Percentage of overspending.

        Returns:
        - None
        """
        print(f"Preparing to send email to {to_email}")
        subject = "Overspending Detected"
        content = f"Overspending detected in the {payment_category} category.\n"
        content += f"You have overspent by {overspending_percent:.2f}% compared to the previous month."
        self.email_service.send_email(to_email, subject, content)
        print(f"Email successfully sent to {to_email}")

budget_monitor = BudgetMonitor(PaymentEntryService(), EmailService(api_key=api_key, from_email=from_email), UserService())

def get_date_ranges():
    """
    Generate date ranges for the current and previous months.

    Returns:
    - Dictionary with start and end dates for the current and previous months.
    """
    today = datetime.today()
    first_day_current_month = datetime(today.year, today.month, 1)
    last_day_current_month = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
    first_day_prev_month = datetime(today.year, today.month - 1, 1)
    last_day_prev_month = datetime(today.year, today.month, 1) - timedelta(days=1)
    
    date_ranges = {
        'current': {'start': first_day_current_month, 'end': last_day_current_month},
        'previous': {'start': first_day_prev_month, 'end': last_day_prev_month}
        }
    return date_ranges

def scheduled_check_budget(app):
    """
    Perform scheduled budget checks for all users and payment categories.

    Parameters:
    - app: Flask application instance.

    Returns:
    - None
    """
    with app.app_context():
        all_users = budget_monitor.user_service.get_all_users()
        for user in all_users:
            user_id = user.get('user_id')
            if user_id is not None:
                for payment_category in PaymentCategory:
                    date_range = get_date_ranges()
            
                    budget_monitor.is_over_spending(user_id, payment_category.value, date_range)
