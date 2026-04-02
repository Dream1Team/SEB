import json
import logging
from datetime import datetime

from aiokafka import AIOKafkaProducer

from config import settings

logger = logging.getLogger(__name__)

class SEServicesEventProducer:
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
        logger.info("Kafka Service продюсер запущен")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka Service продюсер остановлен")

    # Categories
    async def service_category_created(self, category_id: int):
        event = {
            "event_type": "service_category_added",
            "category_id": category_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        await self.producer.send("notifications", event)

    async def service_category_updated(self, category_id: int):
        event = {
            "event_type": "service_category_updated",
            "category_id": category_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        await self.producer.send("notifications", event)

    async def service_category_deleted(self, category_id: int):
        event = {
            "event_type": "service_category_deleted",
            "category_id": category_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        await self.producer.send("notifications", event)

    # Subcategories
    async def service_subcategory_created(self, subcategory_id: int):
        event = {
            "event_type": "service_subcategory_added",
            "subcategory_id": subcategory_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        await self.producer.send("notifications", event)

    async def service_subcategory_updated(self, subcategory_id: int):
        event = {
            "event_type": "service_subcategory_updated",
            "subcategory_id": subcategory_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        await self.producer.send("notifications", event)

    async def service_subcategory_deleted(self, subcategory_id: int):
        event = {
            "event_type": "service_subcategory_deleted",
            "subcategory_id": subcategory_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        await self.producer.send("notifications", event)

    # Vacancies
    async def service_created(self, service_id: int):
        event = {
            "event_type": "service_added",
            "service_id": service_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        await self.producer.send("notifications", event)

    async def service_updated(self, service_id: int):
        event = {
            "event_type": "service_updated",
            "service_id": service_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        await self.producer.send("notifications", event)

    async def service_deleted(self, service_id: int):
        event = {
            "event_type": "service_deleted",
            "service_id": service_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        await self.producer.send("notifications", event)