from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.inline import language_button
from bot.buttons.reply import role_button, back_to_start
from bot.states import EmployerForm, EmployeeForm
from db.models import User

main_router = Router()


@main_router.message(CommandStart())
async def language_start_handler(message: Message, state:FSMContext) -> None:
    chat_id = message.from_user.id
    tg_first_name = message.from_user.first_name
    user = await User.get(telegram_id_=chat_id)
    if not user:
        await User.create(chat_id=chat_id, tg_first_name=tg_first_name)
        await message.answer("Iltimos, tilni tanlang\nПожалуйста, выберите язык", reply_markup=language_button())
    await state.set_state()
    await message.answer(_("Siz kimsiz"), reply_markup=role_button())


@main_router.callback_query(F.data.in_(('ru', 'uz')))
async def start_handler(callback: CallbackQuery):
    await callback.message.answer(_("Salom {}").format(callback.message.from_user.first_name))
    await callback.message.answer(_("Siz kimsiz"), reply_markup=role_button())


@main_router.message(EmployeeForm.main_panel, F.text == __(back_to_start))
@main_router.message(EmployerForm.main_panel, F.text == __(back_to_start))
async def main_(message: Message):
    await message.answer(_("Siz kimsiz"), reply_markup=role_button())
