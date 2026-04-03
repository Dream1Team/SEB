from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from database.db_config import UserSettings
from kafka_config.dependencies import get_kafka_producer
from kafka_config.producer import UserEventProducer
from users.base_auth.dependencies import get_settings, authenticate_user
from users.utils.security import get_hash_password, create_access_token
from users.base_auth.schemes import Token, UserRegister, UserAuth
from database.db_manager import get_user_by_email, add_user
from users.utils.auth_exceptions import incorrect_login_value, user_already_exists, incorrect_email

router = APIRouter(tags=['Базовая аутентификация'], prefix='/base_auth')


@router.post('/register')
async def register_user(user_data: UserRegister,
                        producer: UserEventProducer = Depends(get_kafka_producer)) -> dict:
    user = await get_user_by_email(email=user_data.email)
    if user:
        raise user_already_exists

    user_dict = user_data.model_dump()
    user_dict['password'] = get_hash_password(user_data.password)
    await add_user(**user_dict)

    await producer.user_registered(username=user_dict['username'],
                                    register_type='basic')
    return {'message': 'Вы успешно зарегистрированы!'}

@router.post('/login')
async def auth_user(response: Response,
                    user_data: UserAuth,
                    producer: UserEventProducer = Depends(get_kafka_producer)):
    check = await authenticate_user(email=user_data.email, password=user_data.password)

    if check is None:
        raise incorrect_email

    access_token = create_access_token(data={"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    await producer.user_logged_in(key_par="Email:" + user_data.email,
                                logging_type='basic')

    return {'access_token': access_token, 'refresh_token': None}

@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie(key='users_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}


@router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                settings: Annotated[UserSettings, Depends(get_settings)]):

    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise incorrect_login_value

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(data={"sub": user['email']}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")