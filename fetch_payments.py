class FetchPayments():
    def __init__(self, fetch_payments_api):
        self.fetch_payments_api = fetch_payments_api

    def fetch_payments(self, user_id, year, month):
        return self.fetch_payments_api.fetch_payments(user_id, year, month)
