"""Handling authentication tasks."""

# Standard library imports
from datetime import datetime, timedelta
from typing import Optional, Union

# Third party imports
import bcrypt
import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import ValidationError

from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, SECRET_KEY
from src.models.token import JWTCred, JWTMeta, JWTPayload
from src.models.users import UserInDB, UserPasswordUpdate, UserPublic

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AUthException(BaseException):
    """Custom auth exception."""

    pass


class AuthService:
    """Authenticate class for all authentication."""

    def create_salt_and_hashed_password(
        self, *, plaintext_pwd: str
    ) -> UserPasswordUpdate:
        """Create salt and hashed password."""
        salt = self.generate_salt()
        hashed_password = self.hash_password(pwd=plaintext_pwd, salt=salt)
        return UserPasswordUpdate(salt=salt, password=hashed_password)

    def generate_salt(self) -> str:
        """Generate salt."""
        return bcrypt.gensalt().decode()

    def hash_password(self, *, pwd: str, salt: str) -> str:
        """Hash password."""
        return pwd_context.hash(pwd + salt)

    def verify_password(self, *, pwd: str, salt: str, hashed_pwd: str) -> bool:
        """Verify password."""
        return pwd_context.verify(pwd + salt, hashed_pwd)

    def create_access_token_for_user(
        self,
        *,
        user: Union[UserPublic, UserInDB],
        secret_key: str = str(SECRET_KEY),
        expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> Optional[Union[str, bytes]]:
        """Create access token for user."""
        access_token = None

        if not user:
            return None

        jwt_meta = JWTMeta(
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
        )

        jwt_cred = JWTCred(email=user.email, username=user.username)
        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_cred.dict(),
        )
        access_token = jwt.encode(
            token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM
        )

        return access_token

    def get_data_from_token(self, *, token: str, secret_key: str) -> Optional[str]:
        """Get email from token."""
        try:
            decoded_token = jwt.decode(
                token,
                str(secret_key),
                algorithms=[JWT_ALGORITHM],
            )
            payload = JWTCred(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload.username
