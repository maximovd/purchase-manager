from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.errors.http_error import http_error_handler
from app.api.errors.validaition_error import http422_error_handler
from app.api.routes.api import router as api_router
from app.core.config import PROJECT_NAME, DEBUG, VERSION, ALLOWED_HOSTS, API_PREFIX
from app.core.events import create_start_app_handler, init_celery_app


def get_application() -> FastAPI:
    """Application Fabric."""
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    create_start_app_handler(application)  # TODO Create with application events

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=API_PREFIX)

    celery_app = init_celery_app()
    # celery_app.add_periodic_task("test")  # TODO Add periodic task

    return application


app = get_application()
