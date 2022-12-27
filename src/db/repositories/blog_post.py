"""DB repo for Blog Posts."""

# Standard library imports
import logging
import uuid
from typing import List, Union

import asyncpg

# Third party imports
from databases import Database

from src.db.repositories.base import BaseRepository
from src.models.blog_post import (
    BlogPostInDB,
    BlogPostPublic,
    CreateBlogPost,
    UpdateBlogPost,
)

CREATE_BLOG_POST_QUERY = """
    INSERT INTO blog_post ( title, content, user_uuid, user_username)
    VALUES ( :title, :content, :user_uuid, :user_username)
    RETURNING post_id, title, content, user_uuid, user_username, created_at, updated_at;
"""

GET_BLOG_POST_BY_POST_ID_QUERY = """
    SELECT post_id, title, content, user_uuid, user_username, created_at, updated_at
    FROM blog_post
    WHERE post_id = :post_id;
"""

GET_ALL_BLOG_POSTS = """
    SELECT *
    FROM blog_post
"""


UPDATE_BLOG_POST_BY_POST_ID_QUERY = """
    UPDATE blog_post
    SET title = :title, content = :content
    WHERE post_id = :post_id
    RETURNING post_id, title, content, user_uuid, user_username, created_at, updated_at;
"""

DELETE_BLOG_POST_BY_POST_ID_QUERY = """
    DELETE FROM blog_post
    WHERE post_id = :post_id
    RETURNING post_id;
"""


async def generate_uuid():
    """Generate uuid for user id."""
    return str(uuid.uuid4())


class BlogPostRepository(BaseRepository):
    """All db actions associated with the Users resources."""

    def __init__(self, db: Database) -> None:
        """Initialize db, auth_path and profiles_repo."""
        super().__init__(db)

    async def create_new_blog_post(
        self, *, new_blog_post: CreateBlogPost, user_uuid: str, username: str
    ) -> Union[BlogPostInDB, str]:
        new_blog_post_params = new_blog_post.copy(
            update={
                "user_uuid": user_uuid,
                "user_username": username,
            }
        )
        try:
            created_blog_post = await self.db.fetch_one(
                query=CREATE_BLOG_POST_QUERY, values=new_blog_post_params.dict()
            )
        except asyncpg.ForeignKeyViolationError:
            return "The uuid passed is not present in users table"
        return created_blog_post

    async def get_blog_post(
        self, post_id: int
    ) -> Union[BlogPostInDB, BlogPostPublic, None]:
        """Get blog post data."""
        blog_post = await self.db.fetch_one(
            query=GET_BLOG_POST_BY_POST_ID_QUERY,
            values={"post_id": post_id},
        )
        return blog_post

    async def get_all_blog_post(
        self,
    ) -> List[Union[BlogPostInDB, BlogPostPublic, None]]:
        """Get all blog posts"""
        blog_posts = await self.db.fetch_all(query=GET_ALL_BLOG_POSTS)
        return blog_posts

    async def update_blog_posts(
        self, blog_post_updated_params: UpdateBlogPost, post_id: int
    ) -> Union[BlogPostInDB, BlogPostPublic, None]:
        """Update blog post via post id"""
        new_blog_post_updated_params = blog_post_updated_params.copy(
            update={
                "post_id": post_id,
            }
        )
        updated_post = await self.db.fetch_one(
            query=UPDATE_BLOG_POST_BY_POST_ID_QUERY,
            values=new_blog_post_updated_params.dict(),
        )
        return BlogPostInDB(**updated_post)

    async def delete_blog_post(self, *, post_id: int) -> int:
        """Delete blog post via post id."""
        try:
            return await self.db.execute(
                query=DELETE_BLOG_POST_BY_POST_ID_QUERY,
                values={"post_id": post_id},
            )
        except Exception as e:
            print(e)
            return None
