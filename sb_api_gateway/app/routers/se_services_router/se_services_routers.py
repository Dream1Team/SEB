from fastapi import APIRouter, Request, Path, Depends, Body
# from fastapi.params import Query
from starlette.responses import JSONResponse

from app.schemes.services_schemes import SEServicesScheme
from app.services.service_service import service_service
# from dependencies import get_current_admin

router = APIRouter(prefix="/se_services", tags=["Services"])

# UPDATE, GET_SERVICES, CREATE


# Services
@router.get("/services")
async def get_services(request: Request):
    """Получение услуг"""
    result = await service_service.get_services(request)
    # result.update(request.headers.get("Cookie"))
    return JSONResponse(content=result)

#
# @router.get("/services/filter")
# async def get_services_by_filter(request: Request,
#                                  params: ServicesQuery = Query(...)):
#     """Получение услуг по фильтру"""
#     result = await service_service.get_vacancies_by_filter(request=request,
#                                                           params=params.model_dump())
#
#     return JSONResponse(content=result)


@router.get("/services/subcategory/{subcat_id}")
async def get_services_by_subcategory_id(request: Request,
                                         subcat_id: int = Path(...)):
    """Получение услуг по ID подкатегории"""
    result = await service_service.get_services_by_subcategory_id(request, subcat_id)

    return JSONResponse(content=result)


@router.get("/services/{service_id}")
async def get_service_by_id(request: Request,
                             service_id: int = Path(...)):
    """Получение услуги по ID"""
    result = await service_service.get_service_by_id(request, service_id)
    return JSONResponse(result)


@router.post("/services")
async def create_service(request: Request,
                         service_data: SEServicesScheme = Body(...)):
    """Добавление товаров"""
    result = await service_service.create_service(request, service_data=service_data.model_dump(by_alias=True))

    return JSONResponse(content=result)

@router.put("/services/{service_id}")
async def update_service(request: Request,
                          service_data: SEServicesScheme = Body(...),
                          service_id: int = Path(...)):
    result = await service_service.update_service(request,
                                                  service_id=service_id,
                                                  service_data=service_data.model_dump(by_alias=True))
    return JSONResponse(content=result)

@router.delete("/services/{service_id}")
async def delete_service(request: Request,
                         service_id: int = Path(...)):
    result = await service_service.delete_service(request, service_id)

    return JSONResponse(content=result)


@router.get("/health")
async def health(request: Request):
    pass