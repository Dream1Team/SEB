import logging
import sys

from dotenv import load_dotenv
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router
from kafka_config.dependencies import (get_kafka_producer, get_kafka_consumer,
                                       stop_consumer, _producer_client)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Управление жизненным циклом приложения.
    """
    logger.info("🚀 Запуск сервиса товаров...")

    await get_kafka_producer()
    await get_kafka_consumer()

    yield

    # Shutdown
    if _producer_client:
        await _producer_client.stop()

    await stop_consumer()

load_dotenv(override=True)

app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

if __name__ == "__main__":
    logger.info(f"Hello, Product's Server")
    uvicorn.run('main:app', host='localhost', port=8006)

