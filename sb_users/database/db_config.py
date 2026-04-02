import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class UserSettings(BaseSettings):
    # Database
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # GOOGLE
    GOOGLE_PROJECT_ID: str
    GOOGLE_PROJECT_NUMBER: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URL: str

    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_USERNAME: str

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

    # Secure
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    AFTER_AUTH_REDIRECT_URL: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    def get_auth_data(self):
        return {'secret_key': self.SECRET_KEY, 'algorithm': self.ALGORITHM}


if __name__ == "__main__":
    settings = UserSettings()

    print(settings.GOOGLE_PROJECT_ID)
    print(settings.GOOGLE_PROJECT_NUMBER)
    print(settings.GOOGLE_CLIENT_ID)
    print(settings.GOOGLE_CLIENT_SECRET)
    print(settings.GOOGLE_REDIRECT_URL)