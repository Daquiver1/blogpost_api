"""A model for the blog post"""

from src.models.core import CoreModel, DateTimeModelMixin


class BlogPostBase(CoreModel):
    """Blog Post Model"""

    title: str
    content: str
    username: str


class CreateBlogPost(BlogPostBase):
    """Blog Post Model used for creating a new Blog Post"""

    pass


class BlogPostPublic(BlogPostBase, DateTimeModelMixin):
    """Public Blog Post model"""

    pass


class BlogPostInDB(BlogPostBase, DateTimeModelMixin):
    """Blog Post Model in Database"""

    post_uuid: str
    user_uuid: str
