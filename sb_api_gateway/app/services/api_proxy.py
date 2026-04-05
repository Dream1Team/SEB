import httpx
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException

from dependencies import get_service_url


class ApiProxy:
    category_path: str | None = None
    subcategory_path: str | None = None

    def __init__(self, service_name: str):
        self.base_url = get_service_url(service_name)

    async def proxy_request(
            self,
            method: str,
            path: str,
            request: Request,
            headers: Optional[Dict[str, str]] = None,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None
            ) -> httpx.Response:
        """Базовый запрос к сервису"""

        url = f"{self.base_url}{path}"

        proxy_headers = {}
        if headers:
            proxy_headers.update(headers)

        auth_header = request.headers.get("Authorization")
        if auth_header:
            proxy_headers["Authorization"] = auth_header

        cookie_header = request.cookies.get("users_access_token")
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
                    timeout=30.0,
                    follow_redirects=True
                )

                return response

            except httpx.ConnectError:
                raise HTTPException(
                    status_code=503,
                    detail=f"Product service is unavailable"
                )

            except httpx.TimeoutException:
                raise HTTPException(
                    status_code=504,
                    detail="Product service timeout"
                )

            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=e.response.text
                )

    # Category
    async def get_categories(self, request: Request):
        """Получение всех категорий"""
        response = await self.proxy_request(
            method="GET",
            path=self.category_path,
            request=request
        )

        return response.json()

    async def get_category_by_id(self, request: Request, category_id: int):
        """Получение категории по ID"""
        response = await self.proxy_request(
            method="GET",
            path=f"{self.category_path}{category_id}",
            request=request
        )

        return response.json()

    async def create_category(self, request: Request, cat_data: Dict[str, Any]):
        """Добавление категории"""
        response = await self.proxy_request(
            method="POST",
            path=self.category_path,
            request=request,
            data=cat_data
        )

        return response.json()

    async def update_category(
            self,
            request: Request,
            category_id: int,
            cat_data: Dict[str, Any]
            ):
        """Изменение категории"""
        response = await self.proxy_request(
            method="PUT",
            path=f"{self.category_path}{category_id}",
            request=request,
            data=cat_data
        )

        return response.json()

    async def delete_category(
            self,
            request: Request,
            category_id: int
            ):
        """Удаление категории"""
        response = await self.proxy_request(
            method="DELETE",
            path=f"{self.category_path}{category_id}",
            request=request
        )

        return response.json()

    # Subcategory
    async def get_subcategories(self, request: Request):
        """Получение всех подкатегорий"""
        response = await self.proxy_request(
            method="GET",
            path=self.subcategory_path,
            request=request
        )

        return response.json()

    async def get_subcategory_by_id(self, request: Request, subcat_id: int):
        """Получение подкатегории по ID"""
        response = await self.proxy_request(
            method="GET",
            path=f"{self.subcategory_path}{subcat_id}",
            request=request
        )

        return response.json()

    async def get_subcategories_by_cat_id(self, request: Request, cat_id: int):
        """Получение подкатегорий по ID категории"""
        response = await self.proxy_request(
            method="GET",
            path=f"{self.subcategory_path}category/{cat_id}",
            request=request
        )

        return response.json()

    async def create_subcategory(
            self,
            request: Request,
            subcat_data: Dict[str, Any]
            ):
        """Добавление подкатегории"""
        response = await self.proxy_request(
            method="POST",
            path=self.subcategory_path,
            request=request,
            data=subcat_data
        )

        return response.json()

    async def update_subcategory(
            self,
            request: Request,
            subcat_id: int,
            subcat_data: Dict[str, Any]
            ):
        """Изменение подкатегории"""
        response = await self.proxy_request(
            method="PUT",
            path=f"{self.subcategory_path}{subcat_id}",
            request=request,
            data=subcat_data
        )

        return response.json()

    async def delete_subcategory(
            self,
            request: Request,
            subcat_id: int
            ):
        """Удаление подкатегории"""
        response = await self.proxy_request(
            method="DELETE",
            path=f"{self.subcategory_path}{subcat_id}",
            request=request
        )

        return response.json()