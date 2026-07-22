from datetime import datetime, date
from typing import Optional


def calculate_age(dob: str) -> int:
    """
    Calculate age from date of birth.

    Args:
        dob: Date of birth in YYYY-MM-DD format.

    Returns:
        Age in years.
    """
    if not dob:
        return 0

    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.now()

        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )

        return max(0, age)

    except Exception:
        return 0


def get_age_group(age: int) -> str:
    """
    Determine age group.

    Args:
        age: Age in years.

    Returns:
        Age group category.
    """
    if age < 18:
        return "Child"
    elif age < 40:
        return "Young Adult"
    elif age < 65:
        return "Adult"
    else:
        return "Senior"


def format_date(
    date_str: str,
    input_format: str = "%Y-%m-%d",
    output_format: str = "%B %d, %Y",
) -> str:
    """
    Convert date format.
    """
    try:
        dt = datetime.strptime(date_str, input_format)
        return dt.strftime(output_format)

    except Exception:
        return date_str


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Convert a date string into a datetime object.
    """
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)

        except Exception:
            continue

    return None