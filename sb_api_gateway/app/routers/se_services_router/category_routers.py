from fastapi import APIRouter, Request, Path, Body
from starlette.responses import JSONResponse

from app.schemes.services_schemes import CategoryScheme
from app.services.service_service import service_service
# from dependencies import get_current_admin


router = APIRouter(prefix="/se_services", tags=["Service's categories"])


# Categories
@router.get("/categories", summary="Получение категорий вакансий")
async def get_service_categories(request: Request):
    result = await service_service.get_categories(request)
    return JSONResponse(content=result)


@router.get("/categories/{cat_id}", summary="Получение категории услуг по ID")
async def get_service_category_by_id(request: Request,
                                     cat_id: int = Path(...)):
    result = await service_service.get_category_by_id(request, cat_id)
    return JSONResponse(result)


@router.post("/categories", summary="Добавление категории услуг")
async def create_category(request: Request,
                          category_data: CategoryScheme = Body(...)):
    result = await service_service.create_category(request, cat_data=category_data.model_dump(by_alias=True))
    return JSONResponse(result)


@router.put("/categories/{cat_id}", summary="Обновление категории")
async def update_category(request: Request,
                          category_data: CategoryScheme = Body(...),
                          cat_id: int = Path(...)):
    result = await service_service.update_category(request, cat_id, category_data.model_dump(by_alias=True))
    return JSONResponse(result)


@router.delete("/categories/{cat_id}", summary="Удаление категории")
async def delete_category(request: Request,
                          cat_id: int = Path(...)):
    result = await service_service.delete_category(request, cat_id)
    return JSONResponse(result)