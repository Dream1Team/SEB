from typing import Optional

from jose import jwt, JWTError

from config import settings


def verify_token(token: str) -> Optional[str]:
    """Проверка токена"""
    # settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_sub = payload.get("sub")
        if token_sub is None:
            return None
        return token_sub
    except JWTError:
        return None