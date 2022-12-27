"""A model for the user"""

from typing import Annotated, Optional

from pydantic import EmailStr, Field

from src.models.core import CoreModel, DateTimeModelMixin
from src.models.token import AccessToken


class UserBase(CoreModel):
    """User Base Model"""

    email: EmailStr
    first_name: str
    last_name: str
    username: str


class CreateUser(UserBase):
    """User Model used for creating a new user"""

    password: Annotated[str, Field(min_length=7, max_length=80)]


class UserPasswordUpdate(CoreModel):
    """Generated password and salt."""

    uuid: str
    password: Annotated[str, Field(min_length=7, max_length=80)]
    salt: str


class UserInDB(UserBase, DateTimeModelMixin):
    """User Model in Database"""

    uuid: str
    password: Annotated[str, Field(min_length=7, max_length=80)]
    salt: str


class UserPublic(UserBase, DateTimeModelMixin):
    """Public user model"""

    access_token: Optional[AccessToken]
