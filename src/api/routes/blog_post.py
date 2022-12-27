"""Router for Users."""

# Third party imports
from typing import List, Union

from fastapi import APIRouter, Depends, Form, HTTPException, status

from src.api.dependencies.auth import get_current_active_user
from src.api.dependencies.database import get_repository
from src.core.config import TOKEN_TYPE
from src.db.repositories.blog_post import BlogPostRepository
from src.models.blog_post import BlogPostPublic, CreateBlogPost, UpdateBlogPost
from src.models.users import UserInDB, UserPublic
from src.services.auth import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post(
    "/create",
    response_model=BlogPostPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_blog_post(
    title: str = Form(...),
    content: str = Form(...),
    current_user: UserInDB = Depends(get_current_active_user),
    blog_post_repo: BlogPostRepository = Depends(get_repository(BlogPostRepository)),
) -> UserPublic:
    """Create a new user."""
    new_blog_post = CreateBlogPost(
        title=title,
        content=content,
    )
    created_blog_post = await blog_post_repo.create_new_blog_post(
        new_blog_post=new_blog_post,
        user_uuid=current_user.uuid,
        username=current_user.username,
    )

    return created_blog_post


@router.get("/get/", response_model=Union[BlogPostPublic, str])
async def get_blog_post(
    post_id: int,
    current_client: str = Depends(get_current_active_user),
    blog_post_repo: BlogPostRepository = Depends(get_repository(BlogPostRepository)),
):
    """Get blog post."""

    result = await blog_post_repo.get_blog_post(post_id)
    if result:
        return result
    return "No blog post found"


@router.get(
    "/get_all/",
    response_model=List[BlogPostPublic],
)
async def get_all_blog_post(
    current_client: str = Depends(get_current_active_user),
    blog_post_repo: BlogPostRepository = Depends(get_repository(BlogPostRepository)),
):
    """Get all blog post."""

    return await blog_post_repo.get_all_blog_post()


@router.put("/update/", response_model=BlogPostPublic)
async def update_blog_post(
    post_id: int,
    title: str,
    content: str,
    current_user: UserInDB = Depends(get_current_active_user),
    blog_post_repo: BlogPostRepository = Depends(get_repository(BlogPostRepository)),
) -> UserPublic:
    """Update user route."""
    updated_blog_post = UpdateBlogPost(title=title, content=content)
    return await blog_post_repo.update_blog_posts(
        blog_post_updated_params=updated_blog_post, post_id=post_id
    )


@router.delete(
    "/delete",
    response_model=Union[int, None],
    status_code=status.HTTP_200_OK,
)
async def delete_blog_post(
    post_id: int,
    current_user: UserInDB = Depends(get_current_active_user),
    blog_post_repo: BlogPostRepository = Depends(get_repository(BlogPostRepository)),
) -> str:
    """Delete blog post"""
    return await blog_post_repo.delete_blog_post(post_id=post_id)
