from loguru import logger

from app.models import Products, StatusTypes
from app.services.utils import async_to_sync, task_lock
from app.worker.worker import celery_app


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    sender.add_periodic_task(20.0, sync_clean_done_task.s())


@celery_app.task(bind=True)
def sync_clean_done_task(self) -> None:
    """Convert async func to sync."""
    async_to_sync(run_lock_task, self)


async def run_lock_task(self):
    lock_id = f'{self.name}-lock'
    async with task_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            return await clean_done_purchase()
        logger.info(f'{self.name} - already running')


async def clean_done_purchase() -> None:
    """Task for clean purchase with status DONE."""
    async for product in Products.all():
        if product.status == StatusTypes.DONE:
            await product.delete()
            logger.info(f'Purchase <{product.id}> was deleted because it was in the {product.status} state')
