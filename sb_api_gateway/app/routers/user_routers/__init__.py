from fastapi import APIRouter

from app.routers.user_routers.base_routers import router as base_router
from app.routers.user_routers.google_routers import router as google_router
from app.routers.user_routers.telegram_routers import router as telegram_router


router = APIRouter()


router.include_router(base_router)
router.include_router(google_router)
router.include_router(telegram_router)