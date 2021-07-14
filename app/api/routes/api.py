from fastapi import APIRouter

from app.api.routes import categories

router = APIRouter()
router.include_router(categories.router, tags=["categories"], prefix="/categories")
