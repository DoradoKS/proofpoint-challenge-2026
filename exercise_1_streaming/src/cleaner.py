import re
from datetime import datetime

def clean_number(value: str) -> int:
    """Converts a string to a number, if the number has an invalid format, it is set to 0."""
    if not value or not str(value).strip():
        return 0
    
    try:
        num = int(str(value).strip())
        return num if num >= 0 else 0
    except ValueError:
        return 0

def clean_string(value: str, default: str = "") -> str:
    """Removes trailing spaces from text. If empty or missing, returns the default value provided."""
    if not value or not str(value).strip():
        return default
    return str(value).strip()

def normalize_for_comparison(value: str) -> str:
    """Normalizes a string to be compared looking for duplicates."""
    if not value:
        return ""
    lowered = str(value).lower()
    collapsed = re.sub(r'\s+', ' ', lowered).strip()
    
    return collapsed

def clean_date(value: str) -> str:
    """Checks if Air Date is valid, if it is missing, empty, or an impossible date, it returns 'Unknown'."""
    if not value or not str(value).strip():
        return "Unknown"
    val_str = str(value).strip()

    try:
        datetime.strptime(val_str, "%Y-%m-%d")
        return val_str
    except ValueError:
        return "Unknown"