import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI


from api import router
from kafka_config.dependencies import (get_kafka_producer, get_kafka_consumer,
                                       stop_consumer, _producer_client)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Управление жизненным циклом приложения.
    """
    logger.info("🚀 Запуск сервиса вакансий...")

    await get_kafka_producer()
    await get_kafka_consumer()

    yield

    # Shutdown
    if _producer_client:
        await _producer_client.stop()

    await stop_consumer()

load_dotenv(override=True)

app = FastAPI(lifespan=lifespan, title="Сервис услуг самозанятых")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run('main:app', host='localhost', port=8007)