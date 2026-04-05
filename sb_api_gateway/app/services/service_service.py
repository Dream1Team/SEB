from typing import Dict, Any

from fastapi import HTTPException, Request

from app.services.api_proxy import ApiProxy


class ServiceService(ApiProxy):
    """Сервис для проксирования запросов к Services микросервису"""
    category_path = "/se_services_module/categories/"
    subcategory_path = "/se_services_module/subcategories/"

    def __init__(self, service_name: str):
        super().__init__(service_name)

    # Services
    async def get_services(self, request: Request):
        """Получение всех услуг"""
        response = await self.proxy_request(
            method="GET",
            path="/se_services_module/se_services/",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Services list is empty")
            )

        return response.json()
    #
    # async def get_services_by_filter(self,
    #                                  request: Request,
    #                                  params: Dict[str, Any]) -> Dict[str, Any]:
    #     response = await self.proxy_request(
    #         method="GET",
    #         path="/se_services_module/se_services/filter",
    #         params=params,
    #         request=request
    #     )
    #
    #     if response.status_code != 200:
    #         raise HTTPException(
    #             status_code=response.status_code,
    #             detail=response.json().get("detail", "Services list is empty")
    #         )
    #
    #     return response.json()

    async def get_services_by_subcategory_id(self,
                                             request: Request,
                                             subcat_id: int):
        """Получение услуг по ID подкатегории"""
        response = await self.proxy_request(
            method="GET",
            path=f"/se_services_module/se_services/subcategory/{subcat_id}",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Services not found")
            )

        return response.json()

    async def get_service_by_id(self,
                                request: Request,
                                service_id: int):
        """Получение услуги по ID"""
        response = await self.proxy_request(
            method="GET",
            path=f"/se_services_module/se_services/{service_id}",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Service not found")
            )

        return response.json()

    async def create_service(self,
                             request: Request,
                             service_data: Dict[str, Any]):
        """Добавление услуги"""
        response = await self.proxy_request(
            method="POST",
            path="/se_services_module/se_services/",
            request=request,
            data=service_data
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Service creating failed")
            )

        return response.json()

    async def update_service(self,
                             request: Request,
                             service_id: int,
                             service_data: Dict[str, Any]):
        """Изменение услуги"""
        response = await self.proxy_request(
            method="PUT",
            path=f"/se_services_module/se_services/{service_id}",
            request=request,
            data=service_data
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Service updating failed")
            )

        return response.json()

    async def delete_service(self,
                             request: Request,
                             service_id: int):
        """Удаление услуги"""
        response = await self.proxy_request(
            method="DELETE",
            path=f"/se_services_module/se_services/{service_id}",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Service deleting failed")
            )

        return response.json()


service_service = ServiceService(service_name="services")