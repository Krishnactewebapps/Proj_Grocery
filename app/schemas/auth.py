from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class RegistrationRequest(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: constr(min_length=8)

class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerificationRequest(BaseModel):
    email: EmailStr
    otp: constr(min_length=6, max_length=6)

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
