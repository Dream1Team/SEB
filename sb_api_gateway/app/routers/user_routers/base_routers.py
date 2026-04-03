from fastapi import APIRouter, Request, Depends, Body, Response
from fastapi.responses import JSONResponse, RedirectResponse

from app.schemes.user_schemes import UserRegister, UserAuth
from app.services.auth_service import user_service
from dependencies import get_current_user_id

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register_user(
    request: Request,
    user_data: UserRegister = Body(...)
):
    """Регистрация пользователя"""
    result = await user_service.register(request, user_data.model_dump())
    return JSONResponse(content=result)


@router.post("/login")
async def login_user(
    request: Request,
    response: Response,
    user_data: UserAuth = Body(...)
):
    """Авторизация пользователя"""
    result = await user_service.login(request=request,
                                      resp=response,
                                      user_data=user_data.model_dump())

    token = result.get("access_token")

    return {"users_access_token": token}


@router.post("/logout")
async def logout_user(request: Request,
                      response: Response):
    """Выход из системы"""
    await user_service.logout(request, response)
    response.delete_cookie(key="users_access_token")
    
    return {'message': 'Пользователь успешно вышел из системы'}