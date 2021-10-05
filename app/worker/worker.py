from celery import Celery

from app.core.config import REDIS_SERVER, BROKER_URI

celery_app = Celery(
    "worker",
    backend=REDIS_SERVER,
    broker=BROKER_URI,
)

