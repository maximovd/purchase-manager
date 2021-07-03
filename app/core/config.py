import logging
import sys
from typing import List

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from app.core.logging import InterceptHandler

# Base config

API_PREFIX = "/api"

VERSION = "0.1.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

# Database config

DATABASE_URL: str = config("DB_CONNECTION", cast=str)
MAX_CONNECTION_COUNT: int = config("MAX_CONNECTION_COUNT", cast=int, default=10)
MIN_CONNECTION_COUNT: int = config("MIN_CONNECTION_COUNT", cast=int, default=10)

# Security config

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

PROJECT_NAME: str = config("PROJECT_NAME", default="Purchase manager")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOST",
    cast=CommaSeparatedStrings,
    default="",
)

# Logging Conf

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])