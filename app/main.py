from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import PROJECT_NAME, DEBUG, VERSION, ALLOWED_HOSTS
from app.core.events import create_start_app_handler


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
    application.add_event_handler("startup", create_start_app_handler(application))

    return application


app = get_application()
