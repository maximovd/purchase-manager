from celery.schedules import crontab
from loguru import logger

from app.core.events import init_celery_app, async_to_sync
from app.models import Products, StatusTypes

celery_app = init_celery_app()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    sender.add_periodic_task(crontab(hour=00, minute=0), sync_clean_done_task.s())


@celery_app.task
def sync_clean_done_task() -> None:
    """Convert async func to sync."""
    async_to_sync(clean_done_purchase_task)


async def clean_done_purchase_task():
    """Task for clean purchase with status DONE."""
    async for product in Products.all():
        if product.status == StatusTypes.DONE:
            await product.delete()
            logger.info(f'Purchase <{product.id}> was deleted because it was in the {product.status} state')
