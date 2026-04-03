from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
# from jwt import InvalidTokenError

from users.utils.security import verify_password, get_settings
from database.db_config import UserSettings
from database.db_manager import get_user_by_email, get_user_by_id
from users.utils.auth_exceptions import credentials_exception, end_token_time, user_id_not_found, \
    user_not_found, not_enough_rights


oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def authenticate_user(email: str, password: str):
    """Аутентификация пользователя"""
    user = await get_user_by_email(email=email)
    print('USER', user.password)
    if not user:
        return False
    if not verify_password(password=password, hashed_password=user.password):
        return False
    return user

async def get_current_user(settings: Annotated[UserSettings, Depends(get_settings)], token: Annotated[str, Depends(oauth_scheme)]):
    """Верификация токена и возврат пользователя и метода аутентификации"""
    try:
        payload = jwt.decode(token, settings['secret_key'], algorithms=settings['algorithm'])
    except Exception:
        raise credentials_exception

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise end_token_time

    user_id = payload.get('sub')
    if not user_id:
        raise user_id_not_found

    user = await get_user_by_id(int(user_id))
    if not user:
        raise user_not_found

    return user

# async def get_current_active_user(current_user_data: Annotated[dict, Depends(get_current_user)]):
#     """Верификация, если пользователь активен, либо возврат исключения"""
#     user = current_user_data["user"]
#     auth_method = current_user_data["auth_method"]
#
#     if user["disabled"]:
#         raise HTTPException(status_code=400, detail="Inactive user")
#
#     return {"user": user, "auth_method": auth_method}

async def get_current_admin_user(current_user = Depends(get_current_user)):
    """Проверка прав администратора"""
    if current_user.is_admin:
        return current_user
    raise not_enough_rights