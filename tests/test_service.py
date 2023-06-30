import smtplib
from models import Email
from email_service import send_smtp_email
import pytest
from unittest.mock import patch


@pytest.fixture
def mock_smtp_server():
    class MockSMTPServer:
        def __init__(self, server, port):
            pass

        def starttls(self):
            pass

        def login(self, username, password):
            pass

        def send_message(self, msg):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    return MockSMTPServer


def test_send_smtp_email(mock_smtp_server):
    email = Email(
        to="recipient@example.com",
        subject="Hello",
        message="This is a test email"
    )

    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp.return_value.__enter__.return_value.send_message.side_effect = None

        try:
            send_smtp_email(email)
        except Exception as e:
            pytest.fail(f"Failed to send email: {e}")


def test_send_smtp_email_smtp_error(mock_smtp_server):
    email = Email(
        to="recipient@example.com",
        subject="Hello",
        message="This is a test email"
    )

    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp.return_value.__enter__.return_value.send_message.side_effect = smtplib.SMTPException("SMTP error occurred")

        with pytest.raises(Exception) as e:
            send_smtp_email(email)

        assert str(e.value) == "SMTP error: SMTP error occurred"


def test_send_smtp_email_authentication_error(mock_smtp_server):
    email = Email(
        to="recipient@example.com",
        subject="Hello",
        message="This is a test email"
    )

    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp.return_value.__enter__.return_value.login.side_effect = smtplib.SMTPAuthenticationError(535, "Authentication failed")

        with pytest.raises(Exception) as e:
            send_smtp_email(email)

        assert str(e.value) == "SMTP authentication error: (535, 'Authentication failed')"
