"""Server Setup."""

# Third party imports
from fastapi import FastAPI

from src.api.routes.blog_post import router as blog_post_router
from src.api.routes.users import router as user_router
from src.core import config, tasks


def get_application() -> FastAPI:
    """Server configs."""
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    # event handlers
    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    @app.get("/", name="index")
    async def index() -> str:
        return "Visit ip_addrESs:8000/docs or localhost8000/docs to view documentation."

    app.include_router(blog_post_router, prefix="/blog_post")
    app.include_router(user_router, prefix="/user")

    return app


app = get_application()
