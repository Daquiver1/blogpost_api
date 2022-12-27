"""Setting up configs."""

# Third party imports
import logging

from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

log = logging.getLogger(__name__)


PROJECT_NAME = "blog-post-api"
VERSION = "1.0"
API_PREFIX = "/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret)

ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=10080
)

JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")
TOKEN_TYPE = config("TOKEN_TYPE", cast=str, default="bearer")


POSTGRES_USERNAME = config("POSTGRES_USERNAME", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str)
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}",
)
