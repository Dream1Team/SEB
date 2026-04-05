from fastapi import APIRouter, Request, Path, Body
from starlette.responses import JSONResponse

from app.schemes.vacancies_schemes import CategoryScheme
from app.services.vacancy_service import vacancy_service
# from dependencies import get_current_admin


router = APIRouter(prefix="/vacancies", tags=["Vacancy's categories"])


# Categories
@router.get("/categories", summary="Получение категорий вакансий")
async def get_vacancy_categories(request: Request):
    result = await vacancy_service.get_categories(request)
    return JSONResponse(content=result)


@router.get("/categories/{cat_id}", summary="Получение категории вакансий по ID")
async def get_vacancy_category_by_id(request: Request,
                                     cat_id: int = Path(...)):
    result = await vacancy_service.get_category_by_id(request, cat_id)
    return JSONResponse(result)


@router.post("/categories", summary="Добавление категории вакансий")
async def create_category(request: Request,
                          category_data: CategoryScheme = Body(...)):
    result = await vacancy_service.create_category(request, cat_data=category_data.model_dump(by_alias=True))
    return JSONResponse(result)


@router.put("/categories/{cat_id}", summary="Обновление категории")
async def update_category(request: Request,
                          category_data: CategoryScheme = Body(...),
                          cat_id: int = Path(...)):
    result = await vacancy_service.update_category(request, cat_id, category_data.model_dump(by_alias=True))
    return JSONResponse(result)


@router.delete("/categories/{cat_id}", summary="Удаление категории")
async def delete_category(request: Request,
                          cat_id: int = Path(...)):
    result = await vacancy_service.delete_category(request, cat_id)
    return JSONResponse(result)