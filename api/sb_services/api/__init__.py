from fastapi import APIRouter

from api.categories.routers import router as cat_router
from api.subcategories.routers import router as subcat_router
from api.se_services.routers import router as se_services_router


router = APIRouter(prefix='/se_services_module')

router.include_router(cat_router)
router.include_router(subcat_router)
router.include_router(se_services_router)