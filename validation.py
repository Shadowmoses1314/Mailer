import re


def validate_email(email: str) -> bool:
    if email is None:
        return False

    # Regular expression pattern for email address validation
    email_pattern = r'^[\w\.-]{1,100}@[\w\.-]{1,255}\.[\w]{1,63}$'
    match = re.match(email_pattern, email)
    return match is not None
