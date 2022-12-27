"""DB repo for Users."""

# Standard library imports
from typing import Union

from databases import Database
from fastapi import HTTPException, status
from pydantic import EmailStr

from src.db.repositories.base import BaseRepository
from src.models.users import CreateUser, UserInDB, UserPublic
from src.services.auth import AuthService
from src.utils.uuids import generate_uuid

auth_service = AuthService()

# Third party imports
REGISTER_NEW_USER_QUERY = """
    INSERT INTO users (uuid, first_name, last_name, username, email, password, salt)
    VALUES (:uuid, :first_name, :last_name, :username, :email, :password, :salt)
    RETURNING uuid, first_name, last_name, username, email, password, salt, created_at, updated_at;
"""

GET_USER_BY_EMAIL_QUERY = """
    SELECT uuid, first_name, last_name, username, email, password, salt, created_at, updated_at
    FROM users
    WHERE email = :email;
"""
GET_USER_BY_USERNAME_QUERY = """
    SELECT uuid, first_name, last_name, username, email, password, salt, created_at, updated_at
    FROM users
    WHERE username = :username;
"""

GET_USER_BY_USER_UUID_QUERY = """
    SELECT uuid, gid, first_name, other_names, nin, address, created_At, updated_At
    FROM users
    WHERE uuid = :uuid;
    """

DELETE_USER_BY_USER_UUID_QUERY = """
    DELETE FROM users
    WHERE uuid = :uuid
    RETURNING uuid;
"""


class UserRepository(BaseRepository):
    """All db actions associated with the user resource."""

    def __init__(self, db: Database) -> None:
        """Initialize db"""
        super().__init__(db)

    async def register_new_user(self, *, new_user: CreateUser) -> UserInDB:
        """Register new user."""
        uuid = generate_uuid()
        email = (new_user.email).lower()
        username = (new_user.username).lower()
        if await self.get_user_by_email(email=email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{new_user.email} is already taken. Register a new email.",
            )
        if await self.get_user_by_username(username=username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{new_user.username} is already taken. Register a new username.",
            )

        user_pwd_update = auth_service.create_salt_and_hashed_password(
            plaintext_pwd=new_user.password
        )  # get hashed salt and hashed password.

        new_user_params = new_user.copy(
            update={
                "uuid": uuid,
                "email": email,
                "password": user_pwd_update.password,
                "salt": user_pwd_update.salt,
            }
        )
        return await self.db.fetch_one(
            query=REGISTER_NEW_USER_QUERY, values=new_user_params.dict()
        )

    async def authenticate_user(
        self, *, username: str, password: str
    ) -> Union[UserPublic, None]:
        """Authenticate user."""
        user = None

        user = await self.get_user_by_username(username=username)

        if not user:
            return None
        if not auth_service.verify_password(pwd=password, salt=user.salt, hashed_pwd=user.password):  # type: ignore
            return None
        return user

    async def get_user_by_uuid(self, uuid: str) -> Union[UserInDB, UserPublic, None]:
        """Get user data"""
        return await self.db.fetch_one(
            query=GET_USER_BY_USER_UUID_QUERY,
            values={"uuid": uuid},
        )

    async def get_user_by_username(
        self, *, username: str
    ) -> Union[UserInDB, UserPublic, None]:
        """Get user by username."""
        user_record = await self.db.fetch_one(
            query=GET_USER_BY_USERNAME_QUERY, values={"username": username}
        )
        return user_record

    async def get_user_by_email(
        self, *, email: Union[EmailStr, str]
    ) -> Union[UserInDB, UserPublic, None]:
        """Get user by email."""
        user_record = await self.db.fetch_one(
            query=GET_USER_BY_EMAIL_QUERY, values={"email": email}
        )
        return user_record

    async def delete_user(self, *, uuid: str) -> str:
        """Delete user data by uuid."""
        return await self.db.execute(
            query=DELETE_USER_BY_USER_UUID_QUERY,
            values={"uuid": uuid},
        )
