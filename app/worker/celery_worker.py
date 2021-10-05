from time import sleep

from celery import current_task

from app.worker.celery_app import celery_app


@celery_app.on_after_configure.connect
def setup_repeated_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, test_celery.s())


@celery_app.task(acks_late=True)
def test_celery() -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': i * 10})
    return "test task return"
