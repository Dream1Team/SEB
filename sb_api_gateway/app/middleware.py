import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware для проверки аутентификации"""

    async def dispatch(self, request: Request, call_next: Callable):
        public_paths = ["/", "/health", "/api/v1/auth", "/api/v1/users/register"]

        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Требуется авторизация"}
            )

        response = await call_next(request)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware для ограничения запросов"""

    def __init__(self, app):
        super().__init__(app)
        self.request_counts = {}

    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = request.client.host
        current_time = time.time()

        # Очистка старых записей (1 минута)
        self._clean_old_requests(current_time)

        # Подсчет запросов
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []

        self.request_counts[client_ip].append(current_time)

        # Проверка лимита
        minute_ago = current_time - 60
        requests_in_minute = [
            t for t in self.request_counts[client_ip]
            if t > minute_ago
        ]

        if len(requests_in_minute) > settings.RATE_LIMIT_PER_MINUTE:
            return JSONResponse(
                status_code=429,
                content={"detail": "Слишком много запросов"}
            )

        response = await call_next(request)
        return response

    def _clean_old_requests(self, current_time: float):
        """Очистка старых записей"""
        minute_ago = current_time - 60
        for ip in list(self.request_counts.keys()):
            self.request_counts[ip] = [
                t for t in self.request_counts[ip]
                if t > minute_ago
            ]
            if not self.request_counts[ip]:
                del self.request_counts[ip]