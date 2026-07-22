import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """
    Validate an email address.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate a phone number.
    """
    # Remove spaces, hyphens, and parentheses
    clean = re.sub(r"[\s\-\(\)]", "", phone)

    return len(clean) >= 10 and clean.isdigit()


def validate_date(
    date_str: str,
    format: str = "%Y-%m-%d",
) -> bool:
    """
    Validate a date string.
    """
    try:
        datetime.strptime(date_str, format)
        return True

    except Exception:
        return False


def validate_required_fields(
    data: dict,
    required_fields: list,
) -> bool:
    """
    Check whether required fields exist in the data.
    """
    return all(field in data for field in required_fields)