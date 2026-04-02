from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.se_services.models import SEServices
from database.dao.base_dao import BaseDAO
from database.db_manager import connection


class ServicesDAO(BaseDAO):
    model = SEServices

    @classmethod
    async def get_services_by_subcat(cls, subcat_id: int, session: AsyncSession = None):
        """Получение услуг по ID подкатегории"""
        transaction = select(cls.model).where(cls.model.subcategory_id == subcat_id)

        result = await session.execute(transaction)

        return result.scalars().all()


class DBServices:
    @connection
    async def get_all_services(self, session: AsyncSession = None):
        result = await ServicesDAO.get_all_entries(session=session)

        return result

    @connection
    async def get_service_by_id(self, id: int, session: AsyncSession = None):
        result = await ServicesDAO.get_entry(_id=id, session=session)
        return result

    @connection
    async def get_services_by_subcategory_id(self, subcat_id: int, session: AsyncSession = None):
        result = await ServicesDAO.get_services_by_subcat(subcat_id=subcat_id, session=session)
        return result

    @connection
    async def create_service(self, session: AsyncSession = None, **values):
        result = await ServicesDAO.add_entry(session=session, **values)
        return result

    @connection
    async def edit_service(self, _id: int, session: AsyncSession = None, **values):
        result = await ServicesDAO.edit_entry(_id=_id, session=session, **values)
        return result

    @connection
    async def delete_service(self, _id: int, session: AsyncSession = None):
        result = await ServicesDAO.del_entry(_id=_id, session=session)
        return result


db_serv = DBServices()
