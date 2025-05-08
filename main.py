import asyncio
import logging
import os
import sys

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.handlers import main_router, employee_router, work_router, employer_router, admin_router
from db.utils import db

dp = Dispatcher()

TOKEN = os.getenv('TOKEN')


async def all_middleware():
    pass


async def on_startup():
    await db.create_all()


async def main() -> None:
    i18n = I18n(path="locales", default_locale='en')
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(main_router, employee_router, work_router, employer_router, admin_router)
    dp.update.middleware(FSMI18nMiddleware(i18n=i18n))
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
