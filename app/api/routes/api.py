from fastapi import APIRouter

from app.api.routes import categories, users

router = APIRouter()
router.include_router(categories.router, tags=["categories"], prefix="/categories")
router.include_router(users.router, tags=["users"], prefix="/users")

