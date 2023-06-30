import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)



def test_send_email_valid(client):
    email_data = {
        "to": "recpient@example.com",
        "subject": "Test Email",
        "message": "This is a test email"
    }
    response = client.post("/send_email", json=email_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully"}


def test_send_email_invalid(client):
    email_data = {
        "to": "invalid_email",
        "subject": "Hello",
        "message": "Test email"
    }
    response = client.post("/send_email", json=email_data)
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["body","to"],"msg":"value is not a valid email address","type":"value_error.email"}]}


def test_send_email_not_subject(client):
    email_data = {
        "to": "recipient@example.com",
        "message": "Test email"
    }
    response = client.post("/send_email", json=email_data)
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["body","subject"],"msg":"field required","type":"value_error.missing"}]}


def test_send_email_not_message(client):
    email_data = {
        "to": "recipient@example.com",
        "subject": "Hello",
    }
    response = client.post("/send_email", json=email_data)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'message'], 'msg': 'field required', 'type': 'value_error.missing'}]}