from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.subcategories.models import Subcategory
from database.dao.base_dao import BaseDAO
from database.db_manager import connection


class SubcategoriesDAO(BaseDAO):
    model = Subcategory

    @classmethod
    async def get_subcat_by_cat(cls, cat_id: int, session: AsyncSession = None):
        """Получение подкатегории по ID категории"""
        transaction = select(cls.model).where(cls.model.category_id == cat_id)

        result = await session.execute(transaction)

        return result.scalars().all()


class DBSubcategories:
    @connection
    async def get_all_subcategories(self, session: AsyncSession = None):
        result = await SubcategoriesDAO.get_all_entries(session=session)
        return result

    @connection
    async def get_subcategory_by_id(self, _id: int, session: AsyncSession = None):
        result = await SubcategoriesDAO.get_entry(_id=_id, session=session)
        return result

    @connection
    async def get_subcategories_by_category(self, cat_id: int, session: AsyncSession = None):
        result = await SubcategoriesDAO.get_subcat_by_cat(cat_id=cat_id, session=session)
        return result

    @connection
    async def create_subcategory(self, session: AsyncSession = None, **values):
        result = await SubcategoriesDAO.add_entry(session=session, **values)
        return result

    @connection
    async def edit_subcategory(self, _id: int, session: AsyncSession = None, **values):
        result = await SubcategoriesDAO.edit_entry(_id=_id, session=session, **values)
        return result

    @connection
    async def delete_subcategory(self, _id: int, session: AsyncSession = None):
        result = await SubcategoriesDAO.del_entry(_id=_id, session=session)
        return result


db_subcat = DBSubcategories()

# print(asyncio.run(db_cat.create_category(name='Test_name', slug='Test_Slug',
#                                          description='Test_Descr', order_index=666,
#                                          is_active=True)))