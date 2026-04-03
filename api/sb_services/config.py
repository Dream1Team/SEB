import os
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_SECURITY_PROTOCOL: str
    KAFKA_SASL_MECHANISM: str
    KAFKA_SASL_USERNAME: str
    KAFKA_SASL_PASSWORD: str

    # Producer настройки
    KAFKA_PRODUCER_ACKS: str
    KAFKA_PRODUCER_RETRIES: int
    KAFKA_PRODUCER_MAX_IN_FLIGHT: int
    KAFKA_PRODUCER_COMPRESSION_TYPE: str

    # Consumer настройки
    KAFKA_CONSUMER_MAX_POLL_RECORDS: int
    KAFKA_CONSUMER_SESSION_TIMEOUT_MS: int
    KAFKA_CONSUMER_HEARTBEAT_INTERVAL_MS: int

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