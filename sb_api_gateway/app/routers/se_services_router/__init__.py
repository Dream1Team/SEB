from fastapi import APIRouter

from app.routers.se_services_router.category_routers import router as category_router
from app.routers.se_services_router.subcategory_routers import router as subcategory_router
from app.routers.se_services_router.se_services_routers import router as services_router


router = APIRouter()

router.include_router(category_router)
router.include_router(subcategory_router)
router.include_router(services_router)