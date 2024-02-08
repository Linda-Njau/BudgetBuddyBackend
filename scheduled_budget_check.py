import os
from flask_api import status
from app.models import PaymentCategory
from app.services.budget_monitor_service import BudgetMonitor, get_date_ranges
from app.services.payment_entry_service import PaymentEntryService
from app.services.email_service import EmailService
from app.services.user_service import UserService


api_key = os.environ.get('SENDGRID_API_KEY')
budget_monitor = BudgetMonitor(PaymentEntryService(), EmailService(api_key=api_key), UserService())

def scheduled_budget_check(app):
    """
    Perform scheduled budget checks for all users and payment categories.
    """
    with app.app_context():
        all_users, http_status = budget_monitor.user_service.get_all_users()
        if http_status == status.HTTP_200_OK:
            for user in all_users:
                user_id = user.get('user_id')
                if user_id is not None:
                    for payment_category in PaymentCategory:
                        date_range = get_date_ranges()
                        budget_monitor.detect_overspending(user_id, payment_category.value, date_range)
