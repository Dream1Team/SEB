from fastapi import APIRouter

from app.routers.user_routers import router as user_router
from app.routers.product_routers import router as products_router
from app.routers.vacancies_routers import router as vacancies_router
from app.routers.se_services_router import router as services_router


router = APIRouter()

router.include_router(user_router)
router.include_router(products_router)
router.include_router(vacancies_router)
router.include_router(services_router)