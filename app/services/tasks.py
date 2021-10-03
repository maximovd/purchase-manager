import time

from celery.schedules import crontab
from loguru import logger

from app.core.events import async_to_sync, celery_app
from app.models import Products, StatusTypes
from app.services.utils import one_task


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    sender.add_periodic_task(crontab(hour=00, minute=0), sync_clean_done_task.s())


@celery_app.task(bind=True)
def sync_clean_done_task(self) -> None:
    """Convert async func to sync."""
    one_task(async_to_sync(clean_done_purchase_task), self)


async def clean_done_purchase_task() -> None:
    """Task for clean purchase with status DONE."""
    async for product in Products.all():
        if product.status == StatusTypes.DONE:
            await product.delete()
            logger.info(f'Purchase <{product.id}> was deleted because it was in the {product.status} state')
        time.sleep(50)
