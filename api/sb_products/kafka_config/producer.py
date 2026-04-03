import asyncio
import json
from datetime import datetime

from aiokafka import AIOKafkaProducer
import logging

from config import settings

logger = logging.getLogger(__name__)

class ProductEventProducer:
    def __init__(self):
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            request_timeout_ms=5000,
            retry_backoff_ms=1000,
            max_batch_size=16384,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks=1,
            linger_ms=5
        )

        await self.producer.start()
        logger.info(f"Kafka Product продюсер запущен")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info(f"Kafka Product продюсер остановлен")

    # Категории
    async def product_category_created(self, cat_name: str, cat_id: int):
        event = {
            "event_type": "product_category_added",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "cat_id": cat_id,
                "cat_name": cat_name
            }
        }

        await self.producer.send("notifications", event)

    async def product_category_updated(self, cat_name: str, cat_id: int):
        event = {
            "event_type": "product_category_updated",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "cat_id": cat_id,
                "cat_name": cat_name
            }
        }

        await self.producer.send("notifications", event)

    async def product_category_deleted(self, cat_id: int):
        event = {
            "event_type": "product_category_deleted",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "cat_id": cat_id
            }
        }

        await self.producer.send("notifications", event)

    # Подкатегории
    async def product_subcategory_created(self, subcat_name: str, subcat_id: int):
        event = {
            "event_type": "product_subcategory_added",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "subcat_id": subcat_id,
                "subcat_name": subcat_name
            }
        }

        await self.producer.send("notifications", event)

    async def product_subcategory_updated(self, subcat_name: str, subcat_id: int):
        event = {
            "event_type": "product_subcategory_updated",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "subcat_id": subcat_id,
                "subcat_name": subcat_name
            }
        }

        await self.producer.send("notifications", event)

    async def product_subcategory_deleted(self, subcat_id: int):
        event = {
            "event_type": "product_subcategory_deleted",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "subcat_id": subcat_id
            }
        }

        await self.producer.send("notifications", event)

    # Товары
    async def product_created(self, product_name: str, product_id: int):
        event = {
            "event_type": "product_added",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "product_id": product_id,
                "product_name": product_name
            }
        }

        await self.producer.send("notifications", event)

    async def product_updated(self, product_name: str, product_id: int):
        event = {
            "event_type": "product_updated",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "product_id": product_id,
                "product_name": product_name
            }
        }

        await self.producer.send("notifications", event)

    async def product_deleted(self, product_id: int):
        event = {
            "event_type": "product_deleted",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "product_id": product_id
            }
        }

        await self.producer.send("notifications", event)


if __name__ == "__main__":
    async def main():
        prod = ProductEventProducer()
        try:
            await prod.start()
            print("✅ Producer запущен")

            # Здесь можно добавить тестовую отправку
            await prod.product_created("Test Product", 999)
            print("✅ Тестовое сообщение отправлено")

            # Ждем немного, чтобы сообщение отправилось
            await asyncio.sleep(2)

        finally:
            await prod.stop()
            print("✅ Producer остановлен")


    asyncio.run(main())