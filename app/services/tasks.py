import celery
from loguru import logger

from app.models import Products, StatusTypes


@celery.task
async def clean_done_purchase_task():
    """Task for clean purchase with status DONE."""
    async for product in Products.all():
        if product.status == StatusTypes.DONE:
            await product.delete()
            logger.info(f'Purchase <{product.id}> was deleted because it was in the {product.status} state')
