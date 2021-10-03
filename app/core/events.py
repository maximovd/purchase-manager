import asyncio
from typing import Callable

from celery import Celery
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import DATABASE_URL, BROKER_URI, REDIS_SERVER


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


def init_celery_app() -> Celery:
    return Celery("worker", backend=REDIS_SERVER, broker=BROKER_URI)


celery_app = init_celery_app()


# TODO Rework this to decorator
async def wrap_db_ctx(func: Callable, *args, **kwargs) -> None:
    """Init db and run task."""
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["models"]})
    await Tortoise.generate_schemas()
    await func(*args, **kwargs)


def async_to_sync(func: Callable, *args, **kwargs) -> None:
    """Convert asynchronous func to synchronous."""
    asyncio.run(wrap_db_ctx(func, *args, **kwargs))


# celery_app.conf.task_routes = {
#     "app.service.task.sync_clean_done_task": "clean_task-queue"
# }
# celery_app.conf.update(task_track_started=True)

celery_app.conf.beat_schedule = {
    "clean_task": {
        "task": "app.service.task.sync_clean_done_task",
        "schedule": 10.0
    }
}
