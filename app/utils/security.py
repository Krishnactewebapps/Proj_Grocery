import hashlib
import hmac
from typing import Any


def hash_value(value: str, salt: str = "") -> str:
    """
    Hash a value (e.g., password) with optional salt using SHA-256.
    """
    value_bytes = (value + salt).encode("utf-8")
    return hashlib.sha256(value_bytes).hexdigest()


def verify_hash(value: str, hashed: str, salt: str = "") -> bool:
    """
    Verify a value against a given hash using the same salt.
    """
    return hash_value(value, salt) == hashed


def secure_compare(val1: Any, val2: Any) -> bool:
    """
    Securely compare two values to prevent timing attacks.
    """
    if isinstance(val1, str):
        val1 = val1.encode("utf-8")
    if isinstance(val2, str):
        val2 = val2.encode("utf-8")
    return hmac.compare_digest(val1, val2)
