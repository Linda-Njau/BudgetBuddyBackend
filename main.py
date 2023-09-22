from datetime import datetime
from app.models import PaymentCategory
from app.api.services import payment_entry_service
from app.models import PaymentCategory
from email_service import EmailService

class BudgetMonitor(object):
    def __init__(self, payment_entry_service, email_service, user_service):
        self.payment_entry_service = payment_entry_service
        self.email_service = email_service
        self.user_service = user_service

    def is_over_spending(self, user_id, payment_category, month):
        now = datetime.utcnow()
        current_month = now.month
        previous_month = current_month -1
        
        current_month_entries = self.payment_entry_service.get_payment_entries(user_id, payment_category, month=current_month)
        previous_month_entries = self.payment_entry_service.get_payment_entries(user_id, payment_category, month=previous_month)
        
        if current_month_entries and previous_month_entries:
            current_month_spending = 0
            previous_month_spending = 0
            
            for entry in current_month_entries:
                current_month_spending += entry["amount"]
                
            for entry in previous_month_entries:
                previous_month_spending += entry["amount"]
                                
            if current_month_spending >= 1.5 * previous_month_spending:
                user_data = self.user_service.get_user(user_id)
                user_email = user_data["email"]
                overspending_percent = ((current_month_spending - previous_month_spending)/ previous_month_spending) * 100
                self.send_overspending_email(user_email, payment_category, overspending_percent)
                return True
            else:
                return False

    def send_overspending_email(self, to_email, payment_category, overspending_percent):
        from_email = "contact@vanoma.com"
        subject = "Overspending Detected"
        content = f"Overspending detected in the {payment_category} category.\n"
        content += f"You have overspent by {overspending_percent:.2f}% compared to the previous month."
        
        
        self.email_service.send_email(from_email, to_email, subject, content)
