from typing import Callable

from celery import Celery
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import DATABASE_URL, BROKER_URI


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


def init_celery_app() -> Celery:
    return Celery(
        "worker",
        backend=BROKER_URI,
        broker=BROKER_URI,
    )
