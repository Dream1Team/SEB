from typing import Optional
import secrets
import asyncio

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse

from kafka_config.producer import UserEventProducer
from kafka_config.dependencies import get_kafka_producer
from users.base_auth.schemes import Token
from database.db_manager import get_user_by_email, add_from_google, update_user_from_google, get_user_by_google_id
from users.google_auth.oauth import GoogleOAuth
from users.utils.auth_exceptions import google_auth_error, auth_code_error, invalid_state_par, invalid_get_tokens, \
    invalid_get_user
from users.utils.security import create_access_token

router = APIRouter(prefix='/google', tags=['Аутентификация Google'])

# Использовать Redis
_state_store = {}

@router.get('/login')
async def google_login(request: Request):
    """Перенаправление на страницу авторизации Google"""

    # Генерируем случайный state для защиты от CSRF
    state = secrets.token_urlsafe(32)
    _state_store[state] = True

    # URL для редиректа после авторизации
    frontend_callback = request.query_params.get("redirect_uri")

    if frontend_callback:
        _state_store[f"{state}_callback"] = frontend_callback
    else:
        _state_store[f"{state}_callback"] = GoogleOAuth.AUTH_REDIRECT_URL

    auth_url = GoogleOAuth.get_auth_url(state)

    return RedirectResponse(auth_url)

@router.get('/callback')
async def google_callback(code: Optional[str] = None,
                          state: Optional[str] = None,
                          error: Optional[str] = None):
    """Callback endpoint для обработки ответа от Google"""

    if error:
        raise google_auth_error

    if not code:
        raise auth_code_error

    if not state or state not in _state_store:
        raise invalid_state_par

    tokens = await GoogleOAuth.get_tokens(code)
    if not tokens:
        raise invalid_get_tokens

    user_info = await GoogleOAuth.get_user_info(tokens["access_token"])
    if not user_info:
        raise invalid_get_user

    user = await get_user_by_email(user_info.email)
    if not user:
        user = await add_from_google(user_info)

    else:
        user = await update_user_from_google(user_id=user.id, google_user=user_info)

    # Создаем JWT токен для нашего API
    access_token = create_access_token(data={"sub": user.id})

    # Получаем URL для редиректа на фронтенд
    frontend_callback = _state_store.get(f"{state}_callback")
    if frontend_callback:
        # Редирект на фронтенд с токеном
        redirect_url = f"{frontend_callback}?token={access_token}"
        return RedirectResponse(redirect_url)
    else:
        # Возвращаем JSON с токеном
        return JSONResponse(
            content={
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "avatar_url": user.avatar_url
                }
            }
        )

@router.post('/token',
             summary='Получение токена',
             response_model=Token)
async def google_token_exchange(request: Request,
                                producer: UserEventProducer = Depends(get_kafka_producer)):
    """Endpoint для SPA приложений (обмен кода на токен)"""
    body = await request.json()
    code = body.get("code")

    if not code:
        raise HTTPException(status_code=400, detail="Code is required")

    # Получаем токены от GOOGLE
    tokens = await GoogleOAuth.get_tokens(code)
    if not tokens:
        raise invalid_get_tokens

    # Получаем информацию о пользователе
    user_info = await GoogleOAuth.get_user_info(tokens["access_token"])
    if not user_info:
        raise invalid_get_user

    user = await get_user_by_email(user_info.email)

    if not user:
        user = await get_user_by_google_id(user_info.sub)

    if not user:
        user = await add_from_google(user_info)
    else:
        user = await update_user_from_google(user=user, google_user=user_info)

    await producer.user_logged_in(key_par="Google ID:" + user.google_id,
                                                   logging_type='Google')

    # Создаем наш JWT токен
    access_token = create_access_token(data={"sub": user.email})

    return Token(
        access_token=access_token,
        token_type="bearer"
    )

