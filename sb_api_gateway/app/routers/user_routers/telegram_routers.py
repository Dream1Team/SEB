from fastapi import APIRouter, Request, Depends, Body
from fastapi.responses import JSONResponse

from app.schemes.user_schemes import TelegramAuthData
from app.services.auth_service import user_service
from dependencies import get_current_user_id

# Маршруты для User сервиса
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/telegram")
async def telegram_auth(
    request: Request,
    telegram_data: TelegramAuthData = Body(...)
):
    """Авторизация через Telegram"""
    result = await user_service.telegram_auth(request, telegram_data)
    return JSONResponse(content=result)


@router.get("/me")
async def get_current_user(
    request: Request,
    user_id: str = Depends(get_current_user_id)
):
    """Получение информации о текущем пользователе"""
    result = await user_service.get_current_user(request)
    return JSONResponse(content=result)


# Пример роутера для Vacancies
vacancies_router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@vacancies_router.get("/")
async def get_vacancies(request: Request):
    """Получение списка вакансий"""
    return {"message": "Vacancies list"}


# Пример роутера для Services
services_router = APIRouter(prefix="/services", tags=["Services"])


@services_router.get("/")
async def get_services(request: Request):
    """Получение списка услуг"""
    return {"message": "Services list"}
