import json
import logging
import asyncio

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from config import settings

logger = logging.getLogger(__name__)

class SEServicesEventConsumer:
    def __init__(self):
        self.is_running = False
        self.consumer = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            # "notifications",
            "user.events",
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v else None,
            group_id='se_services_service',
            auto_offset_reset='latest',
            fetch_min_bytes=1,
            fetch_max_wait_ms=500,
            max_partition_fetch_bytes=1048576,
            connections_max_idle_ms=540000
        )

        self.is_running = True

        await self.consumer.start()

        logger.info("Services consumer запущен")

        asyncio.create_task(self._consume_loop())

    async def stop(self):
        """Останавливает consumer"""
        self.is_running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info(f"Services consumer остановлен")

    async def _consume_loop(self):
        """Основной цикл чтения событий"""
        try:
            async for message in self.consumer:
                event = message.value
                try:
                    if event["event_type"] == "user_registered":
                        ...
                    if event["event_type"] == "user_logged_in":
                        ...
                    if event["event_type"] == "user_updated":
                        ...
                    if event["event_type"] == "user_deleted":
                        ...

                    # # Получаем от API GATEWAY
                    # if event["event_type"] == "service_category_added":
                    #     logger.info("The service's category has been added")
                    # if event["event_type"] == "service_category_updated":
                    #     logger.info("The service's category has been updated")
                    # if event["event_type"] == "service_category_deleted":
                    #     logger.info("The service's category has been deleted")
                    #
                    # if event["event_type"] == "service_subcategory_added":
                    #     logger.info("The service's subcategory has been added")
                    # if event["event_type"] == "service_subcategory_updated":
                    #     logger.info("The service's subcategory has been updated")
                    # if event["event_type"] == "service_subcategory_deleted":
                    #     logger.info("The service's subcategory has been deleted")
                    #
                    # if event["event_type"] == "service_added":
                    #     logger.info("The service has been added")
                    # if event["event_type"] == "service_updated":
                    #     logger.info("The service has been updated")
                    # if event["event_type"] == "service_deleted":
                    #     logger.info("The service has been deleted")

                    await self.consumer.commit()

                except Exception as e:
                    logger.error(f"Ошибка обработки сообщения: {e}", exc_info=True)

        except KafkaError as e:
            logger.error(f"Kafka ошибка: {e}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")

    async def reconnect(self):
        """Переподключение consumer"""
        await self.consumer.stop()
        await asyncio.sleep(5)
        await self.consumer.start()