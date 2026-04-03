from fastapi import APIRouter

from app.routers.vacancies_routers.category_routers import router as category_router
from app.routers.vacancies_routers.subcategory_routers import router as subcategory_router
from app.routers.vacancies_routers.vacancies_routers import router as vacancies_router


router = APIRouter()

router.include_router(category_router)
router.include_router(subcategory_router)
router.include_router(vacancies_router)