import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
print("SENDGRID_API_KEY:", sendgrid_api_key)
from_email = Email("mucunguzia@gmail.com")
to_email = To("lindanjau21@gmail.com")
subject = "Overspending Detected"
content = Content("text/plain","content")
mail = Mail(from_email, to_email, subject, content)

mail_json = mail.get()

response = sg.client.mail.send.post(request_body=mail_json) 
print(response.status_code)
print(response.headers)
print(response.body)


