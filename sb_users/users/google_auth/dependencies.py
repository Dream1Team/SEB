from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database.db_manager import get_user_by_email
from users.utils.auth_exceptions import credentials_exception, user_not_found, inactive_user
from users.utils.security import verify_token

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Получение текущего пользователя из JWT токена"""
    token = credentials.credentials
    email = verify_token(token)

    if email is None:
        raise credentials_exception

    user = await get_user_by_email(email=email)

    if user is None:
        raise user_not_found

    if not user.is_active:
        raise inactive_user

    return user