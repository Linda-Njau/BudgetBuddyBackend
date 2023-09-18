from datetime import datetime
from app.models import PaymentCategory
from app.api.services import payment_entry_service
from app.models import PaymentCategory


class OverSpending(object):
    def __init__(self, payment_entry_service, notification_service):
        self.payment_entry_service = payment_entry_service
        self.notification_service = notification_service
        
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
                print("overspending detected, send email notification")
                from_email = "your@email.com"  # Replace with your email
                to_email = "recipient@email.com"  # Replace with recipient's email
                subject = "Overspending Detected"
                content = "Overspending detected in the {} category for user {}.".format(payment_category, user_id)
                self.notification_service.send_email(from_email, to_email, subject, content)
                return True
            else:
                print("spending normal, do not send email notification")
        return False
