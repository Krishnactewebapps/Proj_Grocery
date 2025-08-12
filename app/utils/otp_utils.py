import random
import string
from datetime import datetime, timedelta


def generate_otp(length: int = 6) -> str:
    """
    Generate a numeric OTP of specified length.
    """
    return ''.join(random.choices(string.digits, k=length))


def is_otp_valid(otp_record: dict, otp: str) -> bool:
    """
    Check if the provided OTP matches and is not expired.
    """
    if not otp_record:
        return False
    if otp_record.get('otp') != otp:
        return False
    expires_at = otp_record.get('expires_at')
    if not expires_at or datetime.utcnow() > expires_at:
        return False
    return True


def get_otp_expiry_time(minutes: int = 5) -> datetime:
    """
    Get the expiry time for an OTP (default 5 minutes from now).
    """
    return datetime.utcnow() + timedelta(minutes=minutes)
