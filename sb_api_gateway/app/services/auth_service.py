import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException, Request, Response

from config import settings
from dependencies import get_service_url


class UserService:
    """Сервис для проксирования запросов к User микросервису"""

    def __init__(self):
        self.base_url = get_service_url("users")

    async def proxy_request(
            self,
            method: str,
            path: str,
            request: Request,
            headers: Optional[Dict[str, str]] = None,
            data: Optional[Dict[str, Any]] = None
            ) -> httpx.Response:
        """Проксирование запроса к User сервису"""

        url = f"{self.base_url}{path}"

        proxy_headers = {}
        if headers:
            proxy_headers.update(headers)

        auth_header = request.headers.get("Authorization")
        if auth_header:
            proxy_headers["Authorization"] = auth_header

        cookie_header = request.headers.get("Cookie")
        if cookie_header:
            proxy_headers["Cookie"] = cookie_header

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=proxy_headers,
                    json=data if data else None,
                    params=dict(request.query_params),
                    timeout=30.0
                )

                return response

            except httpx.ConnectError:
                raise HTTPException(
                    status_code=503,
                    detail=f"User service is unavailable"
                )
            except httpx.TimeoutException:
                raise HTTPException(
                    status_code=504,
                    detail="User service timeout"
                )

    async def register(self, request: Request, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Регистрация пользователя"""
        response = await self.proxy_request(
            method="POST",
            path="/auth/base_auth/register",
            request=request,
            data=user_data
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Registration failed")
            )

        return response.json()

    async def login(self, request: Request, user_data: Dict[str, Any], resp: Response) -> Dict[str, Any]:
        """Авторизация пользователя"""
        response = await self.proxy_request(
            method="POST",
            path="/auth/base_auth/login",
            request=request,
            data=user_data
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Login failed")
            )

        # Проксируем куки из User сервиса
        cookie = response.headers.get("Set-Cookie")

        if cookie:
            try:
                resp.set_cookie(key="users_access_token", value=cookie, httponly=True)
                resp.headers.append("set-cookie", cookie)
            except Exception as e:
                print(f"RESPONSE ERROR: {e}")


        return response.json()

    async def logout(self, request: Request, resp: Response):
        """Выход из системы"""
        response = await self.proxy_request(
            method="POST",
            path="/auth/base_auth/logout",
            request=request
        )

        cookie = response.cookies.get("users_access_token")
        if cookie:
            resp.delete_cookie("users_access_token")

    async def google_login(self, request: Request) -> Dict[str, Any]:
        """Авторизация через Google"""
        response = await self.proxy_request(
            method="GET",
            path="/google/login",
            request=request
        )

        return response.json()

    async def google_callback(self, request: Request) -> Dict[str, Any]:
        """Callback от Google"""
        response = await self.proxy_request(
            method="GET",
            path="/google/callback",
            request=request
        )

        return response.json()

    async def telegram_auth(self, request: Request, telegram_data: Dict[str, Any]) -> Dict[str, Any]:
        """Авторизация через Telegram"""
        response = await self.proxy_request(
            method="POST",
            path="/api/v1/auth/telegram",
            request=request,
            data=telegram_data
        )

        return response.json()

    async def get_current_user(self, request: Request) -> Dict[str, Any]:
        """Получение информации о текущем пользователе"""
        # Определяем тип токена и вызываем соответствующий эндпоинт
        auth_token = request.cookies.get("users_access_token")

        if "telegram" in auth_token.lower():
            # Telegram токен
            response = await self.proxy_request(
                method="GET",
                path="/auth/api/v1/users/me",
                request=request
            )
        else:
            # Basic или Google токен
            response = await self.proxy_request(
                method="GET",
                path="/users/me",  # Нужно добавить этот эндпоинт в User сервис
                request=request
            )

        return response.json()

user_service = UserService()