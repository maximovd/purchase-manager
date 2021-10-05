from celery import Celery

from app.core.config import REDIS_SERVER, BROKER_URI

celery_app = Celery(
    "worker",
    backend=REDIS_SERVER,
    broker=BROKER_URI
)
celery_app.conf.task_routes = {
    "app.worker.celery_worker.test_celery": "test_queue"
}

celery_app.conf.update(task_track_started=True)

# celery_app.conf.beat_schedule = {
#     "clean_task": {
#         "task": "app.worker.celery_worker.test_celery",
#         "schedule": 10.0
#     }
# }
