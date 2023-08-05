from notify_card_holder import NotifyCardHolder
from fetch_payments import FetchPayments


class UnusualSpending(object):
    def __init__(self, fetch_payments, find_unusual_spending, notify_card_holder):
        self.fetch_payments = fetch_payments
        self.find_unusual_spending = find_unusual_spending
        self.notify_card_holder = notify_card_holder
        
    def run(self, user_id):
        self.notify_card_holder.email("42", "high_spending")
        return
        

