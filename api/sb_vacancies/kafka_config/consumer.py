import json
import logging
import asyncio

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from config import settings

logger = logging.getLogger(__name__)

class VacancyEventConsumer:
    def __init__(self):
        self.consumer = None
        self.is_running = False

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            "notifications",
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v else None,
            group_id='vacancies_service',
            auto_offset_reset='latest',
            fetch_min_bytes=1,
            fetch_max_wait_ms=500,
            max_partition_fetch_bytes=1048576,
            connections_max_idle_ms=540000
        )

        self.is_running = True

        await self.consumer.start()

        logger.info("User consumer started")

        asyncio.create_task(self._consume_loop())

    async def stop(self):
        """Останавливает consumer"""
        self.is_running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info(f"User consumer stopped")

    async def _consume_loop(self):
        """Основной цикл чтения событий"""
        try:
            async for message in self.consumer:
                event = message.value
                try:
                    # Получаем от API GATEWAY
                    if event["event_type"] == "vacancy_category_added":
                        logger.info("The vacancy's category has been added")
                    elif event["event_type"] == "vacancy_category_updated":
                        logger.info("The vacancy's category has been updated")
                    elif event["event_type"] == "vacancy_category_deleted":
                        logger.info("The vacancy's category has been deleted")

                    elif event["event_type"] == "vacancy_subcategory_added":
                        logger.info("The vacancy's category has been added")
                    elif event["event_type"] == "vacancy_subcategory_updated":
                        logger.info("The vacancy's category has been updated")
                    elif event["event_type"] == "vacancy_subcategory_deleted":
                        logger.info("The vacancy's category has been deleted")

                    elif event["event_type"] == "vacancy_added":
                        logger.info("The vacancy has been added")
                    elif event["event_type"] == "vacancy_updated":
                        logger.info("The vacancy has been updated")
                    elif event["event_type"] == "vacancy_deleted":
                        logger.info("The vacancy has been deleted")

                    await self.consumer.commit()

                    logger.debug(
                        f"Сообщение из 'Gateway'"
                        f"{event['event_type']}"
                    )
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
