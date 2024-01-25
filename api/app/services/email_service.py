import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailService:
    def __init__(self, api_key):
        """
        A service for sending emails using the SendGrid API.

        Parameters:
        - api_key (str): The API key for the SendGrid service.
        """
        
        self.sg = sendgrid.SendGridAPIClient(api_key=api_key)
        self.from_email = os.getenv("FROM_EMAIL_ADDRESS")

    def send_email(self, to_email, subject, content):
        """
        Send an email using SendGrid API.

        Parameters:
        - to_email (str): The recipient's email address.
        - subject (str): The subject of the email.
        - content (str): The content of the email.

        Returns:
        - status_code (int): The HTTP status code of the email sending request.
        - headers (dict): The headers received in the response.
        """
        to_email = To(to_email)
        content = Content("text/plain", content)
        mail = Mail(self.from_email, to_email, subject, content)

        mail_json = mail.get()

        response = self.sg.client.mail.send.post(request_body=mail_json)
        return response.status_code, response.headers
