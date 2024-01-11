import pytest
from app.api.services.budget_monitor_service import BudgetMonitor
from unusual_spending.email_service import EmailService
from unusual_spending.app.api.services.payment_entry_service import PaymentEntryService
from unusual_spending.app.api.services.user_service import UserService
@pytest.fixture
def budget_monitor_instance():
    payment_entry_service = PaymentEntryService()
    email_service = EmailService()
    user_service = UserService()
    
    return