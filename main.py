from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import logging
from app_logger import setup_logger
from validation import validate_email
from email_service import send_smtp_email
from models import Email

load_dotenv()

app = FastAPI()
setup_logger()


@app.post("/send_email")
async def send_email(email: Email):
    if not validate_email(email.to):
        raise HTTPException(status_code=422, detail="Invalid email address")

    try:
        send_smtp_email(email)
        return {"message": "Email sent successfully"}
    except Exception as e:
        logging.exception("Error sending email")
        raise HTTPException(
            status_code=500, detail="Failed to send email: " + str(e))
