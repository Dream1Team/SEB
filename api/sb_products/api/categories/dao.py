from sqlalchemy.ext.asyncio import AsyncSession

from api.categories.models import Category
from database.dao.base_dao import BaseDAO
from database.db_manager import connection


class CategoriesDAO(BaseDAO):
    model = Category


class DBCategories:
    @connection
    async def get_all_categories(self, session: AsyncSession = None):
        result = await CategoriesDAO.get_all_entries(session=session)
        return result

    @connection
    async def get_category_by_id(self, _id: int, session: AsyncSession = None):
        result = await CategoriesDAO.get_entry(_id=_id, session=session)
        return result

    @connection
    async def create_category(self, session: AsyncSession = None, **values):
        result = await CategoriesDAO.add_entry(session=session, **values)
        return result

    @connection
    async def edit_category(self, _id: int, session: AsyncSession = None, **values):
        result = await CategoriesDAO.edit_entry(_id=_id, session=session, **values)
        return result

    @connection
    async def delete_category(self, _id: int, session: AsyncSession = None):
        result = await CategoriesDAO.del_entry(_id=_id, session=session)
        return result


db_cat = DBCategories()
