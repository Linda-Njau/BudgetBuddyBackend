"""from datetime import datetime
from notify_card_holder_wrapper import NotifyCardHolderWrapper
from fetch_payments_wrappper import FetchPaymentsWrapper


class UnusualSpending(object):
    def __init__(self, fetch_payments_wrapper, find_unusual_spending, notify_card_holder_wrapper):
        self.fetch_payments_wrapper : FetchPaymentsWrapper = fetch_payments_wrapper
        self.find_unusual_spending = find_unusual_spending
        self.notify_card_holder_wrapper : NotifyCardHolderWrapper = notify_card_holder_wrapper
        
    def is_unusual_spending(self, user_id):
        now = datetime.utcnow()
        current_month = now.month
        previous_month = current_month -1
        
        current_month_payments = self.fetch_payments_wrapper.fetch_payments(user_id, current_month)
        previous_month_payments = self.fetch_payments_wrapper.fetch_payments(user_id, previous_month)
        
        if current_month_payments and previous_month_payments:
            for category in current_month_payments:
                current_month_spending = current_month_payments.get(category, 0)
                previous_month_spending = previous_month_payments.get(category, 0)
            
            if current_month_spending >= 1.5 * previous_month_spending:
                print("overspending detected, send email notification")
                return True
            else:
                print("spending normal, do not send email notification")
        return False
                
    def run(self, user_id):
        if self.is_unusual_spending(user_id):
            self.notify_card_holder_wrapper.email(user_id, "high_spending")"""

