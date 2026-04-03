from fastapi import APIRouter, Request, Path, Body, Depends
from starlette.responses import JSONResponse

from app.schemes.services_schemes import SubcategoryScheme
from app.services.service_service import service_service
# from dependencies import get_current_admin

router = APIRouter(prefix="/se_services", tags=["Service's subcategories"])


# Subcategories
@router.get("/subcategories")
async def get_service_subcategories(request: Request):
    """Получение подкатегорий товаров"""
    result = await service_service.get_subcategories(request)
    # result.update(request.headers.get("Cookie"))
    return JSONResponse(content=result)


@router.get("/subcategories/{subcat_id}")
async def get_service_subcategory_by_id(request: Request,
                                        subcat_id: int = Path(...)):
    """Получение категории товаров по ID"""
    result = await service_service.get_subcategory_by_id(request, subcat_id)
    return JSONResponse(result)


@router.post("/subcategories")
async def create_subcategory(request: Request,
                             subcategory_data: SubcategoryScheme = Body(...)):
    """Добавление категории товаров"""
    result = await service_service.create_subcategory(request, subcat_data=subcategory_data.model_dump(by_alias=True))
    return JSONResponse(result)


@router.put("/subcategories/{subcat_id}")
async def update_subcategory(request: Request,
                            subcategory_data: SubcategoryScheme = Body(...),
                            subcat_id: int = Path(...)):
    result = await service_service.update_subcategory(request, subcat_id, subcategory_data.model_dump(by_alias=True))
    return JSONResponse(result)


@router.delete("/subcategories/{subcat_id}")
async def delete_subcategory(request: Request,
                            subcat_id: int = Path(...)):
    result = await service_service.delete_subcategory(request, subcat_id)
    return JSONResponse(result)


@router.get("/subcategories/category/{cat_id}")
async def get_subcategories_by_category_id(request: Request,
                                           cat_id: int = Path(...)):
    """Получение подкатегорий по ID категории"""
    result = await service_service.get_subcategories_by_cat_id(request, cat_id)
    return JSONResponse(result)