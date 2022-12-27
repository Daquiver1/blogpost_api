"""create main tables

Revision ID: 8abf6304a9e7
Revises: 
Create Date: 2022-12-27 13:37:16.724675

"""
from typing import Tuple

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8abf6304a9e7"
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    """Update timestamp trigger."""
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    """Create timestamp in DB."""
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def create_users_table() -> None:
    """Create Users Table"""
    op.create_table(
        "users",
        sa.Column("uuid", sa.String, primary_key=True),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("first_name", sa.Text, nullable=False),
        sa.Column("last_name", sa.Text, nullable=False),
        sa.Column("username", sa.String, unique=True, nullable=False, index=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_time
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )


def create_blog_post_table() -> None:
    """Create Blog Post Table"""
    op.create_table(
        "blog_post",
        sa.Column("post_id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.Text),
        sa.Column(
            "user_uuid",
            sa.String,
            sa.ForeignKey("users.uuid", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("user_username", sa.String, nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_blog_post_time
            BEFORE UPDATE
            ON blog_post
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column()
        """
    )


def upgrade() -> None:
    """Upgrade DB"""
    create_updated_at_trigger()
    create_users_table()
    create_blog_post_table()


def downgrade() -> None:
    """Downgrade DB"""
    op.drop_table("blog_post")
    op.drop_table("users")
    op.execute("DROP FUNCTION update_updated_at_column")
