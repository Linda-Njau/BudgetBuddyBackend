import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailService:
    def __init__(self, api_key, from_email):
        self.sg = sendgrid.SendGridAPIClient(api_key=api_key)
        self.from_email = from_email

    def send_email(self, to_email, subject, content):

        from_email = "contact@vanoma.com"
        to_email = To(to_email)
        content = Content("text/plain", content)
        mail = Mail(from_email, to_email, subject, content)

        mail_json = mail.get()
        print("mail_json:", mail_json)

        response = self.sg.client.mail.send.post(request_body=mail_json)
        return response.status_code, response.headers
