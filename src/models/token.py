"""Model for token data."""

# Standard library imports
from datetime import datetime, timedelta

from pydantic import EmailStr

from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.models.core import CoreModel

# Third party imports


class JWTMeta(CoreModel):
    """Model for JWT MetaData."""

    issuer: str = "blogpost-api"
    issued_at: float = datetime.timestamp(datetime.utcnow())
    expires_at: float = datetime.timestamp(
        datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


class JWTCred(CoreModel):
    """Identify users model."""

    email: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCred):
    """Model for JWT Payload."""

    pass


class AccessToken(CoreModel):
    """Model for Access token."""

    access_token: str
    token_type: str
