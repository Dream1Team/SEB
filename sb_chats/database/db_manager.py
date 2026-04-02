from datetime import datetime
from functools import wraps

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from database.db_config import ChatSettings

chat_settings = ChatSettings()

DB_URL = chat_settings.get_database_url()

engine = create_async_engine(url=DB_URL)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


def connection(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'session' in kwargs and kwargs['session'] is not None:
            return await func(*args, **kwargs)

        async with async_session() as session:
            kwargs['session'] = session
            try:
                result = await func(*args, **kwargs)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise

    return wrapper

