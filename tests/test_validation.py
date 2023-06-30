import pytest
from validation import validate_email


@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("test@example.com", True),
        ("user.name@example.co.uk", True),
        ("firstname.lastname1234@example-domain.com", True),
        ("invalid_email", False),
        ("user@example", False),
        ("user@example.", False),
        ("user@.com", False),
        ("", False),
        (None, False),
        ("user_123@example.com", True),
        ("user-name@example.com", True),
        ("user+name@example.com", False),
        ("TEST@EXAMPLE.COM", True),
        ("  test@example.com  ", False),
        ("пользователь@пример.рф", True),
        ("a" * 100 + "@example.com", True),
        ("test@" + "a" * 255 + ".com", True),
        ("test@" + "a" * 256 + ".com", False),
        ("test@example." + "a" * 63, True),
        ("test@example." + "a" * 64, False),
    ],
)
def test_validate_email(email, expected_result):
    assert validate_email(email) is expected_result
