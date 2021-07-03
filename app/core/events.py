from tortoise.contrib.fastapi import register_tortoise

from app.core.config import DATABASE_URL


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
