from fastapi import APIRouter, Request, Path, Depends, Body
from fastapi.params import Query
from starlette.responses import JSONResponse

from app.schemes.vacancies_schemes import VacancyScheme, VacanciesQuery
from app.services.vacancy_service import vacancy_service
# from dependencies import get_current_admin

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


# Products
@router.get("/vacancies")
async def get_vacancies(request: Request):
    """Получение товаров"""
    result = await vacancy_service.get_vacancies(request)
    # result.update(request.headers.get("Cookie"))
    return JSONResponse(content=result)


@router.get("/vacancies/filter")
async def get_vacancies_by_filter(request: Request,
                                 params: VacanciesQuery = Query(...)):
    """Получение товаров по фильтру"""
    result = await vacancy_service.get_vacancies_by_filter(request=request,
                                                          params=params.model_dump(by_alias=True))

    return JSONResponse(content=result)


@router.get("/vacancies/subcategory/{subcat_id}")
async def get_vacancies_by_subcategory_id(request: Request,
                                         subcat_id: int = Path(...)):
    """Получение товаров по ID подкатегории"""
    result = await vacancy_service.get_vacancies_by_subcategory_id(request, subcat_id)

    return JSONResponse(content=result)


@router.get("/vacancies/{vacancy_id}")
async def get_vacancy_by_id(request: Request,
                             vacancy_id: int = Path(...)):
    """Получение товара по ID"""
    result = await vacancy_service.get_vacancy_by_id(request, vacancy_id)
    return JSONResponse(result)


@router.post("/vacancies")
async def create_vacancy(request: Request,
                         vacancy_data: VacancyScheme = Body(...)):
    """Добавление товаров"""
    result = await vacancy_service.create_vacancy(request, vacancy_data=vacancy_data.model_dump(by_alias=True))

    return JSONResponse(content=result)

@router.put("/vacancies/{vacancy_id}")
async def update_vacancy(request: Request,
                          vacancy_data: VacancyScheme = Body(...),
                          vacancy_id: int = Path(...)):
    result = await vacancy_service.update_vacancy(request,
                                                  vacancy_id=vacancy_id,
                                                  vacancy_data=vacancy_data.model_dump(by_alias=True))
    return JSONResponse(content=result)

@router.delete("/vacancies/{vacancy_id}")
async def delete_vacancy(request: Request,
                         vacancy_id: int = Path(...)):
    result = await vacancy_service.delete_vacancy(request, vacancy_id)

    return JSONResponse(content=result)


@router.get("/health")
async def health(request: Request):
    pass