import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete


class BaseDAO:
    model = None

    @classmethod
    async def get_all_entries(cls, session: AsyncSession = None):
        """Шаблон для получения всех записей таблицы"""
        transaction = select(cls.model)

        result = await session.execute(transaction)

        return result.scalars().all()

    @classmethod
    async def get_entry(cls, _id: int, session: AsyncSession = None):
        """Шаблон для получения конкретной записи из таблицы"""
        transaction = select(cls.model).where(cls.model.id == _id)

        result = await session.execute(transaction)

        return result.scalar_one_or_none()

    @classmethod
    async def add_entry(cls, session: AsyncSession = None, **values):
        """Шаблон для добавления записи в таблицу"""
        new_entry = cls.model(**values)

        try:
            session.add(instance=new_entry)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return new_entry

    @classmethod
    async def edit_entry(cls, _id: int, session: AsyncSession = None, **values):
        """Шаблон для изменения записи в таблице"""
        transaction = select(cls.model).where(cls.model.id == _id)

        entry = await session.execute(transaction)

        exists_entry = entry.scalar_one_or_none()

        if not exists_entry:
            return None

        for key, value in values.items():
            if hasattr(exists_entry, key):
                setattr(exists_entry, key, value)

        try:
            await session.commit()
            await session.refresh(exists_entry)
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return exists_entry

    @classmethod
    async def del_entry(cls, _id: int, session: AsyncSession = None):
        """Шаблон для удаления записи из таблицы"""
        transaction = delete(cls.model).where(cls.model.id == _id)

        try:
            await session.execute(transaction)
            await session.commit()

            return True

        except SQLAlchemyError as e:
            await session.rollback()
            print(e)
            return False


# if __name__ == "__main__":
#     dao = BaseDAO()
#     print(asyncio.run(dao.get_all_entries()))