from fastapi.exceptions import HTTPException
from fastapi import status

credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Could not validate credentials",
                                      headers={"WWW-Authenticate": "Bearer"})

incorrect_login_value = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='Неверное имя пользователя или пароль',
                                      headers={'WWW-Authenticate': 'Bearer'})

user_already_exists = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail='Пользователь уже существует')

incorrect_email = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Неверная почта или пароль')

token_not_found = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Токен не найден')

end_token_time = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен истек')

user_id_not_found = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Не найден ID пользователя')

user_not_found = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail='Пользователь не найден')

inactive_user = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail='Пользователь не активен')

not_enough_rights = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                  detail='Недостаточно прав!')

google_auth_error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail='Ошибка авторизации GOOGLE')

auth_code_error = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Код авторизации не поддерживается')

invalid_state_par = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail='Невалидный параметр состояния')

invalid_get_tokens = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                   detail='Ошибка получения токена от GOOGLE')

invalid_get_user = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail='Ошибка получения пользователя от GOOGLE')

invalid_telegram_data = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='Некорректные данные Телеграм')

tel_auth_data_old = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Данные для аутентификации устарели')


