from functools import wraps

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings


DATABASE_URL = settings.get_url()

engine = create_async_engine(url=DATABASE_URL)

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