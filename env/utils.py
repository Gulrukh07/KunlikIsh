from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Bot:
    TOKEN = getenv("TOKEN")
    ADMIN = getenv("ADMIN")

class DB:
    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_NAME")
    DB_PASSWORD = getenv("DB_NAME")
    DB_HOST = getenv("DB_NAME")
    DB_PORT = getenv("DB_NAME")

    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_PORT}"


class Env:
    bot = Bot()
    db = DB()