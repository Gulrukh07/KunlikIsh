from os import getenv

from dotenv import load_dotenv

load_dotenv('/home/gulrukh/PycharmProjects/KunlikIsh/.env')


class Bot:

    TOKEN = getenv("TOKEN")
    ADMIN = getenv("ADMIN")

class DB:
    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_USERNAME")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")

    DB_URL = f"postgresql+asyncpg://postgres:1@{DB_HOST}:{DB_PORT}/{DB_NAME}"



class Env:
    bot = Bot()
    db = DB()