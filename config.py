import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv('.env')


@dataclass
class DatabaseConfig:
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@dataclass
class WebConfig:
    """Web configuration"""
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    USERNAME: str = os.getenv('ADMIN_USERNAME')
    PASSWD: str = os.getenv('ADMIN_PASSWORD')
    DOMAIN: str = os.getenv('WEBHOOK_DOMAIN')


@dataclass
class RedisConfig:
    pass


@dataclass
class BotConfig:
    TOKEN: str = os.getenv("BOT_TOKEN")


@dataclass
class Configuration:
    db = DatabaseConfig()
    redis = RedisConfig()
    bot = BotConfig()
    web = WebConfig()


conf = Configuration()
