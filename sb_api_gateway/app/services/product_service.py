from typing import Dict, Any

from fastapi import HTTPException, Request

from app.services.api_proxy import ApiProxy


class ProductService(ApiProxy):
    """Сервис для проксирования запросов к Products микросервису"""
    category_path = "/products_service/categories/"
    subcategory_path = "/products_service/subcategories/"


    def __init__(self, service_name: str):
        super().__init__(service_name)

    # Products
    async def get_products(self, request: Request):
        """Получение всех товаров"""
        response = await self.proxy_request(
            method="GET",
            path="/products_service/products/",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Product list is empty")
            )

        return response.json()

    async def get_products_by_filter(self,
                                     request: Request,
                                     params: Dict[str, Any]) -> Dict[str, Any]:
        """Получение товаров по фильтру"""
        response = await self.proxy_request(
            method="GET",
            path="/products_service/products/filter",
            params=params,
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Product list is empty")
            )

        return response.json()

    async def get_product_by_id(self,
                                request: Request,
                                product_id: int):
        """Получение товара по ID"""
        response = await self.proxy_request(
            method="GET",
            path=f"/products_service/products/{product_id}",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Product not found")
            )

        return response.json()

    async def get_products_by_subcategory_id(self,
                                             request: Request,
                                             subcat_id: int):
        """Получение товаров по ID подкатегории"""
        response = await self.proxy_request(
            method="GET",
            path=f"/products_service/products/subcategory/{subcat_id}",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Products not found")
            )

        return response.json()

    async def create_product(self,
                             request: Request,
                             product_data: Dict[str, Any]):
        response = await self.proxy_request(
            method="POST",
            path="/products_service/products/",
            request=request,
            data=product_data
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Product creating failed")
            )

        return response.json()

    async def update_product(self,
                             request: Request,
                             product_id: int,
                             product_data: Dict[str, Any]):
        response = await self.proxy_request(
            method="PUT",
            path=f"/products_service/products/{product_id}",
            request=request,
            data=product_data
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Product updating failed")
            )

        return response.json()

    async def delete_product(self,
                             request: Request,
                             product_id: int):
        response = await self.proxy_request(
            method="DELETE",
            path=f"/products_service/products/{product_id}",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Product deleting failed")
            )

        return response.json()


product_service = ProductService(service_name="products")