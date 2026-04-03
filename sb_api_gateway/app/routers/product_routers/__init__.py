from fastapi import APIRouter

from app.routers.product_routers.category_routers import router as category_router
from app.routers.product_routers.subcategory_routers import router as subcategory_router
from app.routers.product_routers.products_routers import router as products_router


router = APIRouter()

router.include_router(category_router)
router.include_router(subcategory_router)
router.include_router(products_router)