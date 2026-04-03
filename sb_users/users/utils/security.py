import hashlib
import hmac
from typing import Optional
from datetime import timedelta, datetime, timezone
from functools import lru_cache

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Request

from database.db_config import UserSettings
from users.telegram_auth.schemes import TokenData
from users.utils.auth_exceptions import token_not_found

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated='auto', default='argon2')

@lru_cache
def get_settings():
    return UserSettings()

def verify_password(password: str, hashed_password: str):
    """Сравнение введенного и хэшированного паролей"""
    return pwd_context.verify(password, hashed_password)

def get_hash_password(password: str):
    """Получение хэша пароля"""
    return pwd_context.hash(password)

def get_token(request: Request):
    """Получение токена"""
    token = request.cookies.get('users_access_token')
    if not token:
        raise token_not_found

    return token

def verify_token(token: str) -> Optional[str]:
    """Проверка токена"""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None

def verify_telegram_token(token: str):
    """Проверка токена от Telegram"""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        telegram_id: int = payload.get("sub")
        if telegram_id is None:
            return None
        return TokenData(telegram_id=telegram_id)
    except JWTError:
        return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Создание токена доступа"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    settings = get_settings()
    auth_data = settings.get_auth_data()
    encoded_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encoded_jwt

def verify_telegram_webapp_data(telegram_data: dict, bot_token: str) -> bool:
    """
    Верификация Telegram Web App данных согласно с:
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
    """
    data_check_string = []
    for key in sorted(telegram_data.keys()):
        if key == 'hash':
            continue
        data_check_string.append(f"{key}={telegram_data[key]}")

    data_check_string = "\n".join(data_check_string)

    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode(),
        digestmod=hashlib.sha256
    ).digest()

    computed_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    return computed_hash == telegram_data.get("hash")
