"""Dependency for authentication."""


# Standard library imports
import logging
from typing import Union

# Third party imports
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.api.dependencies.database import get_repository
from src.core.config import SECRET_KEY
from src.db.repositories.users import UserRepository
from src.models.users import UserInDB, UserPublic

# from src.db.repositories.users import UsersRepository
from src.services.auth import AuthService

auth_service = AuthService()

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="user/authenticate/", scheme_name="JWT")


async def get_user_from_token(
    *,
    token: str = Depends(reuseable_oauth),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> Union[UserInDB, UserPublic, None]:
    """Get user token."""
    try:
        username = auth_service.get_data_from_token(
            token=token, secret_key=str(SECRET_KEY)
        )
        user = await user_repo.get_user_by_username(username=username)
    except Exception:
        raise
    return user


def get_current_active_user(
    current_user: UserInDB = Depends(get_user_from_token),
) -> str:
    """Get current active user from token."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authenticated user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
