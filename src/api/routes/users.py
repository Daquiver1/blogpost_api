"""Router for Users."""

# Third party imports
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from src.api.dependencies.auth import get_current_active_user
from src.api.dependencies.database import get_repository
from src.core.config import TOKEN_TYPE
from src.db.repositories.users import UserRepository
from src.models.token import AccessToken
from src.models.users import CreateUser, UserInDB, UserPublic
from src.services.auth import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post(
    "/create",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def register_new_user(
    email: EmailStr = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserPublic:
    """Create a new user."""
    new_user = CreateUser(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        username=username,
    )
    created_user = await user_repo.register_new_user(new_user=new_user)
    created_user = UserInDB(**created_user)

    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=created_user),
        token_type=TOKEN_TYPE,
    )

    return UserPublic(**created_user.copy(update={"access_token": access_token}).dict())


@router.post(
    "/authenticate/",
    response_model=AccessToken,
)
async def user_authenticate(
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
) -> AccessToken:
    """Authenticate user."""
    user = await user_repo.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication unsuccessful",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=user),
        token_type="bearer",
    )
    return AccessToken(**access_token.dict())


@router.get("/me/", response_model=UserPublic)
async def get_current_user(
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserPublic:
    """Get current user logged in."""
    return current_user


@router.delete(
    "/me/delete",
    response_model=str,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    current_user: UserInDB = Depends(get_current_active_user),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> str:
    """Delete user route."""
    return await user_repo.delete_user(uuid=current_user.uuid)
