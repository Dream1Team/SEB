import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class ChatSettings(BaseSettings):
    # Database
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int

    # Security
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",".env"),
                                        env_file_encoding='utf-8',
                                        extra='ignore')

    def get_database_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    def get_attributes(self):
        return {"secret_key": self.SECRET_KEY, "algorithm": self.ALGORITHM}
