import os
from typing import Optional, List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_NAME: str = "API Gateway"
    SECRET_KEY: str
    AUTH_SECRET_KEY: str
    ALGORITHM: str
    DEBUG: bool = False
    # environment: str = "development"
    ALLOWED_ORIGINS:  List[str]

    # # Proxy
    # timeout: int = 30
    # max_retries: int = 3

    # # JWT
    # JWT_SECRET: str
    # JWT_ALGORITHM: str = "HS256"
    # access_token_expire_minutes: int = 60

    # # OAuth
    # GOOGLE_CLIENT_ID: Optional[str] = None
    # GOOGLE_CLIENT_SECRET: Optional[str] = None
    # TELEGRAM_BOT_TOKEN: Optional[str] = None

    # Микросервисы
    AUTH_SERVICE_URL: str
    AUTH_SERVICE_PORT: int

    PRODUCT_SERVICE_URL: str
    PRODUCT_SERVICE_PORT: int

    VACANCY_SERVICE_URL: str
    VACANCY_SERVICE_PORT: int

    SERVICES_SERVICE_URL: str
    SERVICES_SERVICE_PORT: int

    CHAT_SERVICE_URL: str
    CHAT_SERVICE_PORT: int

    # Настройки кэша
    REDIS_URL: str
    REDIS_CACHE_TTL: int

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str
    # KAFKA_GROUP_ID: str = "api-gateway-group"

    # Redis
    # redis_url: str = "redis://redis:6379"

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # CORS
    # CORS_ORIGINS: list

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))


settings = Settings()