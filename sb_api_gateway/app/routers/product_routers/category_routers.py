from fastapi import APIRouter, Request, Path, Body
from starlette.responses import JSONResponse

from app.schemes.products_schemes import CategoryScheme
from app.services.product_service import product_service
from dependencies import get_current_admin


router = APIRouter(prefix="/products", tags=["Product's categories"])


# Categories
@router.get("/categories", summary="Получение категорий товаров")
async def get_product_categories(request: Request):
    result = await product_service.get_categories(request)
    return JSONResponse(content=result)


@router.get("/categories/{cat_id}", summary="Получение категории товаров по ID")
async def get_product_category_by_id(request: Request,
                                     cat_id: int = Path(...)):
    result = await product_service.get_category_by_id(request, cat_id)
    return JSONResponse(result)


@router.post("/categories", summary="Добавление категории товаров")
async def create_category(request: Request,
                          category_data: CategoryScheme = Body(...)):
    result = await product_service.create_category(request, cat_data=category_data.model_dump(by_alias=True))
    return JSONResponse(result)


@router.put("/categories/{cat_id}", summary="Обновление категории")
async def update_category(request: Request,
                          category_data: CategoryScheme = Body(...),
                          cat_id: int = Path(...)):
    result = await product_service.update_category(request, cat_id, category_data.model_dump(by_alias=True))
    return JSONResponse(result)


@router.delete("/categories/{cat_id}", summary="Удаление категории")
async def delete_category(request: Request,
                          cat_id: int = Path(...)):
    result = await product_service.delete_category(request, cat_id)
    return JSONResponse(result)