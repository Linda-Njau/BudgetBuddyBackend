import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailService:
    def __init__(self, api_key, from_email):
        print("Debug: API Key is", api_key)
        self.sg = sendgrid.SendGridAPIClient(api_key=api_key)
        self.from_email = from_email
        print("Initialized from_email:", self.from_email)

    def send_email(self, to_email, subject, content):

        from_email = "contact@vanoma.com"
        print("from_email:", from_email)
        to_email = To(to_email)
        print("to_email:", to_email)
        content = Content("text/plain", content)
        mail = Mail(from_email, to_email, subject, content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()
        print("mail_json:", mail_json)

        # Send an HTTP POST request to /mail/send
        response = self.sg.client.mail.send.post(request_body=mail_json)
        return response.status_code, response.headers

if __name__ == "__main__":
    # Example usage:
    api_key = os.environ.get('SENDGRID_API_KEY')
    from_email = "contact@vanoma.com"
    to_email = "lindanjau21@gmail.com"
    subject = "OverSpending!"
    content = "and easy to do anywhere, even with Python"

    email_service = EmailService(api_key, from_email)
    status_code, headers = email_service.send_email(to_email, subject, content)
    print(f"Status Code: {status_code}")
    print(f"Headers: {headers}")
