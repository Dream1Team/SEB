import httpx
from typing import Optional

from users.google_auth.schemes import GoogleUserInfo
from users.base_auth.dependencies import get_settings


class GoogleOAuth:
    AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
    AUTH_REDIRECT_URL = "https://game-thrones.com/5-season/46-episode-6.html"  # Изменить

    @staticmethod
    def get_auth_url(state: str | None = None) -> str:
        """Генерация URL для авторизации через Google"""
        from urllib.parse import urlencode
        settings = get_settings()

        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URL,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",  # Для получения refresh токена
            "prompt": "consent"  # Запрос согласия
        }

        if state:
            params["state"] = state

        return f"{GoogleOAuth.AUTH_URL}?{urlencode(params)}"

    @staticmethod
    async def get_tokens(code: str) -> Optional[dict]:
        """Обмен кода авторизации на токены"""
        settings = get_settings()

        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URL
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(GoogleOAuth.TOKEN_URL, data=data)

            if response.status_code != 200:
                return None

            return response.json()

    @staticmethod
    async def get_user_info(access_token: str) -> Optional[GoogleUserInfo]:
        """Получение информации о пользователе"""
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(GoogleOAuth.USER_INFO_URL, headers=headers)

            if response.status_code != 200:
                return None

            user_data = response.json()
            return GoogleUserInfo(
                email=user_data["email"],
                given_name=user_data.get("given_name"),
                family_name=user_data.get("family_name"),
                picture=user_data.get("picture"),
                sub=user_data["sub"],
                email_verified=user_data.get("email_verified", False)
            )

