from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.vacancies.models import Vacancy
from database.dao.base_dao import BaseDAO
from database.db_manager import connection


class VacanciesDAO(BaseDAO):
    model = Vacancy

    @classmethod
    async def get_vac_by_subcat(cls, subcat_id: int, session: AsyncSession = None):
        """Получение подкатегории по ID категории"""
        transaction = select(cls.model).where(cls.model.subcategory_id == subcat_id)

        result = await session.execute(transaction)

        return result.scalars().all()

    @classmethod
    async def get_vacancies_by_filters(cls, session: AsyncSession = None, **values):
        """Получение товаров по фильтрам"""
        transaction = select(cls.model)

        if values.get('../subcategories'):
            transaction = transaction.where(cls.model.subcategory_id.in_(values['subcategories']))

        if values.get('location'):
            transaction = transaction.where(cls.model.location == values['location'])

        if values.get('min_salary'):
            transaction = transaction.where(cls.model.salary_from >= values['min_salary'])

        if values.get('min_salary'):
            transaction = transaction.where(cls.model.salary_to >= values['min_salary'])

        result = await session.execute(transaction)
        return result.scalars().all()


class DBVacancies:
    @connection
    async def get_all_vacancies(self, session: AsyncSession = None):
        result = await VacanciesDAO.get_all_entries(session=session)

        return result

    @connection
    async def get_vacancy_by_id(self, _id: int, session: AsyncSession = None):
        result = await VacanciesDAO.get_entry(_id=_id, session=session)
        return result

    @connection
    async def get_vacancies_by_subcategory_id(self, subcat_id: int, session: AsyncSession = None):
        result = await VacanciesDAO.get_vac_by_subcat(subcat_id=subcat_id, session=session)
        return result

    @connection
    async def get_vacancies_by_filters(self, session: AsyncSession = None, **values):
        result = await VacanciesDAO.get_vacancies_by_filters(session=session, **values)
        return result

    @connection
    async def create_vacancy(self, session: AsyncSession = None, **values):
        result = await VacanciesDAO.add_entry(session=session, **values)
        return result

    @connection
    async def edit_vacancy(self, _id: int, session: AsyncSession = None, **values):
        result = await VacanciesDAO.edit_entry(_id=_id, session=session, **values)
        return result

    @connection
    async def delete_vacancy(self, _id: int, session: AsyncSession = None):
        result = await VacanciesDAO.del_entry(_id=_id, session=session)
        return result


db_vac = DBVacancies()