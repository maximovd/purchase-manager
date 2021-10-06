import asyncio
import time
from contextlib import asynccontextmanager
from typing import Callable

from fastapi_cache.backends.redis import RedisCacheBackend
from loguru import logger
from tortoise import Tortoise

from app.core.config import LOCK_EXPIRE, DATABASE_URL, REDIS_SERVER


@asynccontextmanager
async def task_lock(lock_id: str, oid: str) -> bool:
    cache = RedisCacheBackend(REDIS_SERVER)
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    status = await cache.add(lock_id, oid)
    await cache.expire(lock_id, LOCK_EXPIRE)
    try:
        yield status
    finally:
        logger.info(f"Current time: {time.monotonic()}")
        logger.info(f"Timeout: {timeout_at}")
        logger.info(f"Current status: {status}")
        if time.monotonic() < timeout_at and status is True:
            logger.info(f"Task cache: {lock_id} was delete")
            await cache.delete(lock_id)


async def one_task(fn, self):
    lock_id = f"{self.name}-lock"
    async with task_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            return fn()
        logger.info(f"{self.name} - already running")


def async_to_sync(func: Callable, *args, **kwargs) -> None:
    """Convert asynchronous func to synchronous."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wrap_db_ctx(func, *args, **kwargs))


# TODO Rework this to decorator
async def wrap_db_ctx(func: Callable, *args, **kwargs) -> None:
    """Init db and run task."""
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    await func(*args, **kwargs)
