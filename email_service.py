import smtplib
from email.message import EmailMessage
import os
from models import Email


def send_smtp_email(email: Email):
    msg = EmailMessage()
    msg.set_content(email.message)
    msg['Subject'] = email.subject
    msg['From'] = os.getenv('SMTP_YOUR_GMAIL')
    msg['To'] = email.to

    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    smtp_username = os.getenv('SMTP_YOUR_GMAIL')
    smtp_password = os.getenv('SMTP_PASSWORD')

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        raise Exception("SMTP authentication error: " + str(e))
    except smtplib.SMTPException as e:
        raise Exception("SMTP error: " + str(e))
    except Exception as e:
        raise Exception("Failed to send email: " + str(e))