import os
from datetime import datetime, timedelta
from app import crontab
from app.models import PaymentCategory
from app.api.services import payment_entry_service, user_service
from email_service import EmailService

api_key = os.environ.get('SENDGRID_API_KEY')
from_email = os.environ.get('FROM_EMAIL_ADDRESS')
class BudgetMonitor:
    def __init__(self, payment_entry_service, email_service, user_service):
        self.payment_entry_service = payment_entry_service
        self.email_service = email_service
        self.user_service = user_service

    def calculate_total_spending(self, entries):
        total_spending = 0
        for entry in entries:
            total_spending += entry["amount"]
        return total_spending

    def is_over_spending(self, user_id, payment_category, date_range):
        current_month_entries = self.payment_entry_service.get_payment_entries(
            user_id, payment_category, date_range=date_range['current']
        )
        previous_month_entries = self.payment_entry_service.get_payment_entries(
            user_id, payment_category, date_range=date_range['previous']
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
        print(f"Preparing to send email to {to_email}")
        from_email = "contact@vanoma.com"
        subject = "Overspending Detected"
        content = f"Overspending detected in the {payment_category} category.\n"
        content += f"You have overspent by {overspending_percent:.2f}% compared to the previous month."
        self.email_service.send_email(from_email, to_email, subject, content)

budget_monitor = BudgetMonitor(payment_entry_service, EmailService(api_key=api_key, from_email=from_email), user_service)

def get_date_ranges():
    today = datetime.today()
    first_day_current_month = datetime(today.year, today.month, 1)
    last_day_current_month = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
    first_day_prev_month = datetime(today.year, today.month - 1, 1)
    last_day_prev_month = datetime(today.year, today.month, 1) - timedelta(days=1)
    
    return {
        'current': {'start': first_day_current_month, 'end': last_day_current_month},
        'previous': {'start': first_day_prev_month, 'end': last_day_prev_month}
    }

@crontab.job(minute="*")
def scheduled_check_budget():
    print("Scheduled task started.")
    all_users = user_service.get_all_users()
    print(f"Retrieved all users: {all_users}")
    for user in all_users:
        print(f"Processing user: {user.user_id}")
        user_id = user.user_id
        
        for payment_category in PaymentCategory:
            date_range = get_date_ranges()
    
            budget_monitor.is_over_spending(user_id, payment_category.value, date_range)
