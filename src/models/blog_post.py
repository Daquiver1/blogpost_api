"""A model for the blog post"""

from src.models.core import CoreModel, DateTimeModelMixin, IDModelMixin


class BlogPostBase(CoreModel):
    """Blog Post Model"""

    title: str
    content: str


class CreateBlogPost(BlogPostBase):
    """Blog Post Model used for creating a new Blog Post"""

    pass


class BlogPostPublic(BlogPostBase, DateTimeModelMixin, IDModelMixin):
    """Public Blog Post model"""

    pass


class UpdateBlogPost(BlogPostBase):
    pass


class BlogPostInDB(BlogPostBase, DateTimeModelMixin, IDModelMixin):
    """Blog Post Model in Database"""

    user_uuid: str


class UpdateBlogPostInDB(BlogPostBase, IDModelMixin):
    pass
