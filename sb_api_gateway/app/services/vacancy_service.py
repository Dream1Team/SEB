from typing import Dict, Any

from fastapi import HTTPException, Request

from app.services.api_proxy import ApiProxy


class VacancyService(ApiProxy):
    """Сервис для проксирования запросов к Vacancies микросервису"""

    category_path = "/vac_service/categories/"
    subcategory_path = "/vac_service/subcategories/"

    def __init__(self, service_name: str):
        super().__init__(service_name)

    # Products
    async def get_vacancies(self, request: Request):
        """Получение всех вакансий"""
        response = await self.proxy_request(
            method="GET",
            path="/vac_service/vacancies/",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Vacancies list is empty")
            )

        return response.json()

    async def get_vacancies_by_filter(self,
                                     request: Request,
                                     params: Dict[str, Any]) -> Dict[str, Any]:
        """Получение вакансий по фильтру"""
        response = await self.proxy_request(
            method="GET",
            path="/vac_service/vacancies/filter",
            params=params,
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Vacancies list is empty")
            )

        return response.json()

    async def get_vacancies_by_subcategory_id(self,
                                             request: Request,
                                             subcat_id: int):
        """Получение вакансий по ID подкатегории"""
        response = await self.proxy_request(
            method="GET",
            path=f"/vac_service/vacancies/subcategory/{subcat_id}",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Vacancies not found")
            )

        return response.json()

    async def get_vacancy_by_id(self,
                                request: Request,
                                vacancy_id: int):
        """Получение вакансии по ID"""
        response = await self.proxy_request(
            method="GET",
            path=f"/vac_service/vacancies/{vacancy_id}",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Vacancy not found")
            )

        return response.json()

    async def create_vacancy(self,
                             request: Request,
                             vacancy_data: Dict[str, Any]):
        """Добавление вакансии"""
        response = await self.proxy_request(
            method="POST",
            path="/vac_service/vacancies/",
            request=request,
            data=vacancy_data
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Vacancy creating failed")
            )

        return response.json()

    async def update_vacancy(self,
                             request: Request,
                             vacancy_id: int,
                             vacancy_data: Dict[str, Any]):
        """Изменение вакансии"""
        response = await self.proxy_request(
            method="PUT",
            path=f"/vac_service/vacancies/{vacancy_id}",
            request=request,
            data=vacancy_data
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Vacancy updating failed")
            )

        return response.json()

    async def delete_vacancy(self,
                             request: Request,
                             vacancy_id: int):
        """Удаление вакансии"""
        response = await self.proxy_request(
            method="DELETE",
            path=f"/vac_service/vacancies/{vacancy_id}",
            request=request
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Vacancy deleting failed")
            )

        return response.json()


vacancy_service = VacancyService(service_name="vacancies")