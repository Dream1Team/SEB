from fastapi import APIRouter

from users.base_auth.routers import router as base_router
from users.google_auth.routers import router as google_router
from users.telegram_auth.routers import router as telegram_router


auth_router = APIRouter(prefix='/auth')

auth_router.include_router(base_router)
auth_router.include_router(google_router)
auth_router.include_router(telegram_router)

