from aiogram import Dispatcher

from bot.handlers.work import work_router
from env_data.utils import Env

from bot.handlers.employee import employee_router
from bot.handlers.employer import employer_router
from bot.handlers.main_handler import main_router


TOKEN = Env().bot.TOKEN


dp = Dispatcher()
dp.include_router(main_router)
dp.include_router(employer_router)
dp.include_router(work_router)
dp.include_router(employee_router)