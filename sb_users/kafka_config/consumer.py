import asyncio
import json
import logging
from typing import Optional

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from database.db_manager import user_settings


logger = logging.getLogger(__name__)

class UserEventConsumer:
    def __init__(self):
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.is_running = False

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            "notifications",
            bootstrap_servers=user_settings.KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v else None,
            group_id='users_service',
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
                    if event["event_type"] == "user_registered":
                        logger.info("The user has been registered")
                    elif event["event_type"] == "user_logged_in":
                        logger.info("The user has been logged")
                    elif event["event_type"] == "user_deleted":
                        logger.info("The user has been deleted")
                    elif event["event_type"] == "user_updated":
                        logger.info("The user has been updated")

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