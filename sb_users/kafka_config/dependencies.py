import asyncio
from typing import Optional

# from kafka_config.consumer import UserEventConsumer
# from kafka_config.producer import UserEventProducer

_producer_client = None
_consumer_client = None

async def get_kafka_producer():
    """Зависимость для запуска producer"""
    global _producer_client

    from kafka_config.producer import UserEventProducer

    if _producer_client is None:
        _producer_client = UserEventProducer()
        await _producer_client.start()

    return _producer_client

async def get_kafka_consumer():
    """Зависимость для запуска consumer"""
    global _consumer_client

    from kafka_config.consumer import UserEventConsumer

    # Добавить handler - все доп зависимости

    if _consumer_client is None:
        _consumer_client = UserEventConsumer()

    await _consumer_client.start()

async def stop_consumer():
    """Останавливает consumer"""

    if _consumer_client:
        await _consumer_client.stop()