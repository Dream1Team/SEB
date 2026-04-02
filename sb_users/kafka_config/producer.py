import asyncio
import json
import logging
from datetime import datetime

from aiokafka import AIOKafkaProducer

from database.db_manager import user_settings

logger = logging.getLogger(__name__)

class UserEventProducer:
    def __init__(self):
        self.bootstrap_servers = user_settings.KAFKA_BOOTSTRAP_SERVERS
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
        logger.info("Kafka User продюсер запущен")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka User продюсер остановлен")

    async def user_registered(self, username: int, register_type: str):
        event = {
            "event_type": "user_registered",
            "username": username,
            "register_type": register_type,
            "timestamp": datetime.utcnow().isoformat(),
        }

        await self.producer.send("notifications", event)

    async def user_logged_in(self, key_par: str, logging_type: str):
        event = {
            "event_type": "user_logged_in",
            "user_key_par": key_par,
            'logging_type': logging_type,
            "timestamp": datetime.utcnow().isoformat()
        }

        await self.producer.send("notifications", event)

    # async def user_logouted_in(self, user_mail: int, logging_type: str):
    #     event = {
    #         "event_type": "user_logouted_in",
    #         "user_mail": user_mail,
    #         "timestamp": datetime.utcnow().isoformat()
    #     }
    #
    #     await self.producer.send("notifications", event)

    async def user_updated(self, user_id: int):
        event = {
            "event_type": "user_updated",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        await self.producer.send("notifications", event)

    async def user_deleted(self, user_id: int):
        event = {
            "event_type": "user_deleted",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        await self.producer.send("notifications", event)


kafka_event = UserEventProducer()