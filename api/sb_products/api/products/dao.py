from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.products.models import Product
from database.dao.base_dao import BaseDAO
from database.db_manager import connection


class ProductsDAO(BaseDAO):
    model = Product

    @classmethod
    async def get_products_by_subcat(cls, subcat_id: int, session: AsyncSession = None):
        """Получение товаров по ID подкатегории"""
        transaction = select(cls.model).where(cls.model.subcategory_id == subcat_id)

        result = await session.execute(transaction)

        return result.scalars().all()

    @classmethod
    async def get_products_by_filters(cls, session: AsyncSession = None, **values):
        """Получение товаров по фильтрам"""
        transaction = select(cls.model)

        if values.get('subcategories'):
            transaction = transaction.where(cls.model.subcategory_id.in_(values['subcategories']))

        if values.get('brands'):
            transaction = transaction.where(cls.model.brand.in_(values['brands']))

        if values.get('min_price'):
            transaction = transaction.where(cls.model.price >= values['min_price'])

        if values.get('max_price'):
            transaction = transaction.where(cls.model.price <= values['max_price'])

        if values.get('color'):
            transaction = transaction.where(cls.model.color == values['color'])

        result = await session.execute(transaction)
        return result.scalars().all()


class DBProducts:
    @connection
    async def get_all_products(self, session: AsyncSession = None):
        result = await ProductsDAO.get_all_entries(session=session)

        return result

    @connection
    async def get_product_by_id(self, _id: int, session: AsyncSession = None):
        result = await ProductsDAO.get_entry(_id=_id, session=session)
        return result

    @connection
    async def get_products_by_subcategory_id(self, subcat_id: int, session: AsyncSession = None):
        result = await ProductsDAO.get_products_by_subcat(subcat_id=subcat_id, session=session)
        return result

    @connection
    async def get_products_by_filters(self, session: AsyncSession = None, **values):
        result = await ProductsDAO.get_products_by_filters(session=session, **values)
        return result

    @connection
    async def create_product(self, session: AsyncSession = None, **values):
        result = await ProductsDAO.add_entry(session=session, **values)
        return result

    @connection
    async def edit_product(self, _id: int, session: AsyncSession = None, **values):
        result = await ProductsDAO.edit_entry(_id=_id, session=session, **values)
        return result

    @connection
    async def delete_product(self, _id: int, session: AsyncSession = None):
        result = await ProductsDAO.del_entry(_id=_id, session=session)
        return result


db_prod = DBProducts()