from fastapi import APIRouter

from api.categories.routers import router as cat_router
from api.subcategories.routers import router as subcat_router
from api.vacancies.routers import router as vac_router


router = APIRouter(prefix='/vac_service')

router.include_router(cat_router)
router.include_router(subcat_router)
router.include_router(vac_router)