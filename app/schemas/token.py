from pydantic import BaseModel

class TokenResponse(BaseModel):
    """
    Response model for authentication tokens.

    Attributes:
        access_token (str): The JWT or OAuth2 access token string issued to the client.
        token_type (str): The type of the token issued (e.g., "bearer").
    """
    access_token: str
    token_type: str
