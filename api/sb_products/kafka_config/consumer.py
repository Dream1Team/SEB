import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from config import settings


logger = logging.getLogger(__name__)

class ProductEventConsumer:
    def __init__(self):
        self.consumer = None
        self.is_running = False

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            "notifications",
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v else None,
            group_id='products_service',
            auto_offset_reset='latest',
            fetch_min_bytes=1,
            fetch_max_wait_ms=500,
            max_partition_fetch_bytes=1048576,
            connections_max_idle_ms=540000,
            # client_id='products-service-client'
        )

        self.is_running = True

        await self.consumer.start()

        logger.info("Products Consumer запущен.")

        asyncio.create_task(self._consume_loop())

    async def stop(self):
        """Останавливает consumer"""
        self.is_running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info(f"User consumer stopped")

    async def _consume_loop(self):
        try:
            async for message in self.consumer:
                event = message.value
                try:
                    if event["event_type"] == "product_category_added":
                        logger.info("The product's category has been added.")
                    if event["event_type"] == "product_category_updated":
                        logger.info("The product's category has been updated.")
                    if event["event_type"] == "product_category_deleted":
                        logger.info("The product's category has been deleted.")

                    if event["event_type"] == "product_subcategory_added":
                        logger.info("The product's subcategory has been added.")
                    if event["event_type"] == "product_subcategory_updated":
                        logger.info("The product's subcategory has been updated.")
                    if event["event_type"] == "product_subcategory_deleted":
                        logger.info("The product's subcategory has been deleted.")

                    if event["event_type"] == "product_added":
                        logger.info("The product has been added.")
                    if event["event_type"] == "product_updated":
                        logger.info("The product has been updated.")
                    if event["event_type"] == "product_deleted":
                        logger.info("The product has been deleted.")

                    await self.consumer.commit()

                except Exception as e:
                    logger.error(f"Ошибка обработки сообщения: {e}")

        except KafkaError as e:
            logger.error(f"Ошибка Kafka: {e}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")

    async def reconnect(self):
        """Переподключение consumer"""
        await self.consumer.stop()
        await asyncio.sleep(5)
        await self.consumer.start()


if __name__ == "__main__":
    cons = ProductEventConsumer()
    asyncio.run(cons.start())