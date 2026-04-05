from fastapi import APIRouter, Request, Path, Body, Depends
from starlette.responses import JSONResponse

from app.schemes.products_schemes import SubcategoryScheme
from app.services.product_service import product_service
# from dependencies import get_current_admin

router = APIRouter(prefix="/products", tags=["Product's subcategories"])


# Subcategories
@router.get("/subcategories")
async def get_product_subcategories(request: Request):
    """Получение подкатегорий товаров"""
    result = await product_service.get_subcategories(request)
    # result.update(request.headers.get("Cookie"))
    return JSONResponse(content=result)


@router.get("/subcategories/{subcat_id}")
async def get_product_subcategory_by_id(request: Request,
                                        subcat_id: int = Path(...)):
    """Получение категории товаров по ID"""
    result = await product_service.get_subcategory_by_id(request,
                                                         subcat_id=subcat_id)
    return JSONResponse(content=result)


@router.post("/subcategories")
async def create_subcategory(request: Request,
                             subcategory_data: SubcategoryScheme = Body(...)):
    """Добавление подкатегории товаров"""
    result = await product_service.create_subcategory(request,
                                                      subcat_data=subcategory_data.model_dump(by_alias=True))
    return JSONResponse(content=result)


@router.put("/subcategories/{subcat_id}")
async def update_subcategory(request: Request,
                            subcategory_data: SubcategoryScheme = Body(...),
                            subcat_id: int = Path(...)):
    result = await product_service.update_subcategory(request,
                                                      subcat_id=subcat_id,
                                                      subcat_data=subcategory_data.model_dump(by_alias=True))
    return JSONResponse(content=result)


@router.delete("/subcategories/{subcat_id}")
async def delete_subcategory(request: Request,
                            subcat_id: int = Path(...)):
    result = await product_service.delete_subcategory(request,
                                                      subcat_id=subcat_id)
    return JSONResponse(content=result)


@router.get("/subcategories/category/{cat_id}")
async def get_subcategories_by_category_id(request: Request,
                                           cat_id: int = Path(...)):
    """Получение подкатегорий по ID категории"""
    result = await product_service.get_subcategories_by_cat_id(request,
                                                               cat_id=cat_id)
    return JSONResponse(content=result)