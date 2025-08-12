import re
from typing import Dict, Any
from pydantic import EmailStr, ValidationError


def validate_email(email: str) -> bool:
    """
    Validate email using Pydantic's EmailStr.
    """
    try:
        EmailStr.validate(email)
        return True
    except ValidationError:
        return False


def validate_phone(phone: str) -> bool:
    """
    Validate phone number (simple international format, e.g., +1234567890).
    """
    pattern = re.compile(r"^\+?[1-9]\d{7,14}$")
    return bool(pattern.match(phone))


def validate_profile_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate user profile fields. Returns dict with 'valid' and 'error' keys.
    """
    allowed_fields = {"full_name", "bio", "avatar_url", "email", "phone"}
    for key in fields:
        if key not in allowed_fields:
            return {"valid": False, "error": f"Invalid field: {key}"}
        if key == "email" and not validate_email(fields[key]):
            return {"valid": False, "error": "Invalid email format."}
        if key == "phone" and not validate_phone(fields[key]):
            return {"valid": False, "error": "Invalid phone number format."}
    return {"valid": True}
