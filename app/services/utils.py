import time
from contextlib import asynccontextmanager

from fastapi import Depends
from fastapi_cache import caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from loguru import logger

from app.core.config import LOCK_EXPIRE


def redis_cache():
    return caches.get(CACHE_KEY)


@asynccontextmanager
async def task_lock(lock_id, oid):
    cache: RedisCacheBackend = Depends(redis_cache)
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = await cache.add(lock_id, oid)
    await cache.expire(lock_id, LOCK_EXPIRE)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            await cache.delete(lock_id)


async def one_task(fn, self):
    lock_id = f'{self.name}-lock'
    async with task_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            return fn()
        logger.debug(f'{self.name} - already running')
