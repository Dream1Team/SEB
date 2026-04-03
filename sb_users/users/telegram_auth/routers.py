import asyncio
from datetime import datetime

from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter, Depends

from database.db_manager import get_user_by_telegram_id, add_user_from_telegram, update_user_login
from kafka_config.producer import UserEventProducer
from kafka_config.dependencies import get_kafka_producer
from users.telegram_auth.dependencies import get_current_user
from users.telegram_auth.schemes import Token, TelegramAuthData, UserCreate, UserResponse
from users.utils.auth_exceptions import invalid_telegram_data, tel_auth_data_old
from users.utils.security import verify_telegram_webapp_data, get_settings, create_access_token

router = APIRouter(prefix="/api/v1", tags=["Аутентификация телеграм"])


@router.post("/auth/telegram",
             summary='Авторизация через Telegram',
             response_model=Token)
async def telegram_login(telegram_data: TelegramAuthData,
                        producer: UserEventProducer = Depends(get_kafka_producer)):
    data_dict = telegram_data.model_dump()

    settings = get_settings()

    # Проверяем подпись Telegram
    is_valid = verify_telegram_webapp_data(
        data_dict,
        settings.TELEGRAM_BOT_TOKEN
    )

    if not is_valid:
        raise invalid_telegram_data

    # Проверяем, не устарели ли данные (больше 24 часов)
    auth_date = datetime.fromtimestamp(telegram_data.auth_date)
    if (datetime.now() - auth_date).days > 1:
        raise tel_auth_data_old

    user = await get_user_by_telegram_id(telegram_id=telegram_data.id)

    if not user:
        user_create = UserCreate(**telegram_data.model_dump())
        user = await add_user_from_telegram(user_create)
    else:
        user = await update_user_login(user_id=user.id)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.telegram_id)},
        expires_delta=access_token_expires
    )

    await producer.user_logged_in(key_par="Telegram ID:" + user.telegram_id,
                                   logging_type='Telegram')

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/health")
async def health_status():
    return {"status": "healthy"}