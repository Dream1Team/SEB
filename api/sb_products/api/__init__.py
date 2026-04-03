from fastapi import APIRouter

from api.categories.routers import router as cat_router
from api.subcategories.routers import router as subcat_router
from api.products.routers import router as product_router


router = APIRouter(prefix='/products_service')

router.include_router(cat_router)
router.include_router(subcat_router)
router.include_router(product_router)