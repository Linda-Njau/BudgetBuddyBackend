import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailService:
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    
    def send_email(self, from_email, to_email, subject, content):
        try:
            from_email = Email("mucunguzia@gmail.com")
            to_email = To("lindanjau21@gmail.com")
            subject = "Overspending Detected"
            content = Content("text/plain","content")
            mail = Mail(from_email, to_email, subject, content)
            mail_json = mail.get()
            
            response = self.sg.client.mail.send.post(request_body=mail_json) 
            if response.status_code == 202:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
