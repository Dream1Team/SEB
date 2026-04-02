import logging
import os
import asyncio
from typing import Optional

from contextlib import asynccontextmanager

from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI

from kafka_config.dependencies import (get_kafka_producer, get_kafka_consumer,
                                       _producer_client, stop_consumer)
# from kafka_config.producer import kafka_event
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware

from users import auth_router

# kafka_producer: Optional[UserEventProducer] = None
# kafka_consumer: Optional[ChatEventConsumer] = None

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Управление жизненным циклом приложения.
    """

    logger.info("🚀 Запуск сервиса пользователей...")

    await get_kafka_producer()
    await get_kafka_consumer()

    yield

    # Shutdown
    if _producer_client:
        await _producer_client.stop()

    await stop_consumer()

    # if kafka_producer:
    #     await kafka_producer.stop()


load_dotenv(override=True)

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

origins = [
    "" # url
]

# app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*'],
# )

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run('main:app', host='localhost', port=8002)

    # kafka_event.start()

# username='shima'
# hashed_password='htrh23534ydfb25b245g425h425hj653kmbvcx21'
# first_name='Ilya'
# last_name='Shimanko'
# photo='static/ava.jpg'
# email='shima.228@mail.ru'
# phone='+375333447324'
# birthday='28.07.1997'
# is_active=True
# is_verified=True
# is_admin=False
# is_premium=False
# executor_rating=5.0
# customer_rating=4.3
#
# # Employer
# company_name='Shima Inc.'
# vacancies = ['python-developer', 'nail-master']
#
# # Vacancy-searcher
# portfolio='https://www.github/ShimaCreator'
# resume='resume.docx'
# needed_salary='10000$'
#
# # Self-employed
# se_number='sh14637235'
# services=['nails', 'brows', 'autoservice']
#
# # Seller and Self-employed
# country='Belarus'
# city='Minsk'
# address='Gikalo st. 28, ap.21'