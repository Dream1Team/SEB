import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class DBSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    # Database
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int

    #Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = Field(
        default="localhost:9092",
        description="Список Kafka брокеров через запятую"
    )

    KAFKA_SECURITY_PROTOCOL: Optional[str] = Field(
        default=None,
        description="Протокол безопасности: PLAINTEXT, SASL_SSL, etc"
    )

    KAFKA_SASL_MECHANISM: Optional[str] = Field(
        default=None,
        description="Механизм SASL: PLAIN, SCRAM-SHA-256, SCRAM-SHA-512"
    )

    KAFKA_SASL_USERNAME: Optional[str] = Field(
        default=None,
        description="Имя пользователя для аутентификации"
    )

    KAFKA_SASL_PASSWORD: Optional[str] = Field(
        default=None,
        description="Пароль для аутентификации"
    )

    # Настройки Producer
    KAFKA_PRODUCER_ACKS: str = Field(
        default="all",
        description="Уровень подтверждения: 0, 1, all"
    )

    KAFKA_PRODUCER_RETRIES: int = Field(
        default=5,
        description="Количество повторных попыток отправки"
    )

    KAFKA_PRODUCER_MAX_IN_FLIGHT: int = Field(
        default=5,
        description="Максимальное количество незавершенных запросов"
    )

    KAFKA_PRODUCER_COMPRESSION_TYPE: Optional[str] = Field(
        default=None,
        description="Тип сжатия: gzip, snappy, lz4, zstd"
    )

    # Настройки Consumer
    KAFKA_CONSUMER_MAX_POLL_RECORDS: int = Field(
        default=500,
        description="Максимальное количество записей за один poll"
    )

    KAFKA_CONSUMER_SESSION_TIMEOUT_MS: int = Field(
        default=45000,
        description="Таймаут сессии consumer'а в миллисекундах"
    )

    KAFKA_CONSUMER_HEARTBEAT_INTERVAL_MS: int = Field(
        default=3000,
        description="Интервал heartbeat'ов в миллисекундах"
    )

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
                                                            env_file_encoding='utf-8',
                                                            extra='ignore')

    def get_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/"
                f"{self.DB_NAME}")

settings = DBSettings()


if __name__ == "__main__":
    print(settings.get_url())