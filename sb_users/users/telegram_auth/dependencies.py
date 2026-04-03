from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database.db_manager import  get_user_by_telegram_id
from users.utils.auth_exceptions import credentials_exception, user_not_found, inactive_user
from users.utils.security import verify_telegram_token

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Получение текущего пользователя из JWT токена"""
    token = credentials.credentials
    telegram_id = verify_telegram_token(token)

    if telegram_id is None:
        raise credentials_exception

    user = await get_user_by_telegram_id(telegram_id=telegram_id)

    if user is None:
        raise user_not_found

    if not user.is_active:
        raise inactive_user

    return user