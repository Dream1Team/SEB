from typing import Optional
import jwt

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.exceptions import UnauthorizedException, ForbiddenException
from config import settings

security = HTTPBearer()


async def get_current_user_id(request: Request) -> str:
    """Получение ID текущего пользователя из JWT токена"""
    token = request.cookies.get("access_token")

    if not token:
        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ")[1]

    if not token:
        raise UnauthorizedException("Требуется авторизация")

    try:
        payload = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            raise UnauthorizedException("Неверный токен")

        request.state.user_id = user_id

        return user_id

    except Exception:
        raise UnauthorizedException("Неверный токен")


async def get_current_admin(
        user_id: str = Depends(get_current_user_id)
) -> str:
    """Проверка прав администратора"""
    # Заглушка
    return user_id


def get_service_url(service_name: str) -> str:
    """Получение URL микросервиса по имени"""
    urls = {
        "users": f"http://{settings.AUTH_SERVICE_URL}:{settings.AUTH_SERVICE_PORT}",
        "products": f"http://{settings.PRODUCT_SERVICE_URL}:{settings.PRODUCT_SERVICE_PORT}",
        "vacancies": f"http://{settings.VACANCY_SERVICE_URL}:{settings.VACANCY_SERVICE_PORT}",
        "services": f"http://{settings.SERVICES_SERVICE_URL}:{settings.SERVICES_SERVICE_PORT}",
        "chats": f"http://{settings.CHAT_SERVICE_URL}:{settings.CHAT_SERVICE_PORT}"
    }

    return urls.get(service_name)