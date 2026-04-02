from datetime import datetime
from functools import wraps

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from database.base_models import UserModel
from database.db_config import UserSettings
from users.google_auth.schemes import GoogleUserInfo
from users.telegram_auth.schemes import UserCreate

user_settings = UserSettings()

DB_URL = user_settings.get_db_url()

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

@connection
async def get_user_by_id(user_id: int, session: AsyncSession | None = None):
    """Получение пользователя по ID"""
    transaction = select(UserModel).where(UserModel.id==user_id)

    result = await session.execute(transaction)

    return result.scalar_one_or_none()

@connection
async def get_user_by_email(email: str, session: AsyncSession | None = None):
    """Получение пользователя по email"""
    transaction = select(UserModel).where(UserModel.email == email)

    result = await session.execute(transaction)

    return result.scalar_one_or_none()

@connection
async def get_user_by_username(username: str, session: AsyncSession | None = None):
    """Получение пользователя по username"""
    transaction = select(UserModel).where(UserModel.username == username)

    result = await session.execute(transaction)

    return result.scalar_one_or_none()

@connection
async def get_user_by_google_id(google_id: str,
                                session: AsyncSession | None = None):
    """Получение пользователя по GOOGLE ID"""
    transaction = select(UserModel).where(UserModel.google_id == google_id)

    result = await session.execute(transaction)

    return result.scalar_one_or_none()

@connection
async def get_user_by_telegram_id(telegram_id: int,
                                  session: AsyncSession | None = None):
    """Получение пользователя по Telegram ID"""
    transaction = select(UserModel).where(UserModel.telegram_id == telegram_id)

    result = await session.execute(transaction)

    return result.scalar_one_or_none()

@connection
async def add_user(session: AsyncSession | None = None, **values):
    """Добавление пользователя в БД"""
    transaction = UserModel(**values)

    try:
        session.add(instance=transaction)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise e

    return transaction

@connection
async def add_from_google(google_user: GoogleUserInfo,
                          session: AsyncSession | None = None):
    """Создание данных из пользователя GOOGLE"""
    username = google_user.email.split('@')[0]

    transaction = select(UserModel).where(UserModel.username == username)

    counter = 1
    original_username = username
    while True:
        existing = await session.execute(transaction)

        if existing.scalar_one_or_none() is None:
            break
        username = f"{original_username}{counter}"
        counter += 1

    user = UserModel(
        email=google_user.email,
        username=username,
        first_name=google_user.given_name,
        last_name=google_user.family_name,
        google_id=google_user.sub,
        avatar_url=google_user.picture,
        is_verified=google_user.email_verified
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@connection
async def add_user_from_telegram(user: UserCreate,
                                 session: AsyncSession | None = None):
    new_user = UserModel(
        telegram_id=user.telegram_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        avatar_url=user.avatar_url,
        auth_date=datetime.fromtimestamp(user.auth_date),
        hash=user.hash
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(user)
    return user

@connection
async def update_user_from_google(user_id: int,
                                  google_user: GoogleUserInfo,
                                  session: AsyncSession | None = None):
    """Обновление пользователя из данных GOOGLE"""
    user = await session.get(UserModel, user_id)

    user.google_id = google_user.sub

    if not user.first_name and google_user.given_name:
        user.first_name = google_user.given_name

    if not user.last_name and google_user.family_name:
        user.last_name = google_user.family_name

    if not user.avatar_url and google_user.picture:
        user.avatar_url = google_user.picture

    if not user.is_verified:
        user.is_verified = google_user.email_verified

    await session.commit()
    await session.refresh(user)
    return user

@connection
async def update_user_login(user_id: int,
                            session: AsyncSession | None = None):
    """Обновление последнего входа пользователя из данных Telegram"""
    user = await session.get(UserModel, user_id)
    user.last_login = datetime.now()

    await session.commit()
    await session.refresh(user)

    return user