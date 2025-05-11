from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, I18n

from bot.buttons.inline import language_button
from bot.buttons.reply import role_button
from bot.states import BotState
from db.models import User

main_router = Router()


@main_router.message(CommandStart())
async def language_start_handler(message: Message, state: FSMContext) -> None:
    await  state.set_state(BotState.lang)
    chat_id = message.from_user.id
    tg_first_name = message.from_user.first_name
    user = await User.get(telegram_id_=chat_id)
    if not user:
        await User.create(chat_id=chat_id, tg_first_name=tg_first_name)
        await message.answer("Iltimos, tilni tanlang\nПожалуйста, выберите язык", reply_markup=language_button())
    else:
        await state.set_state()
        await message.answer(_("Siz kimsiz"), reply_markup=role_button())


@main_router.message(Command('language'))
async def language(message: Message, state: FSMContext):
    await state.set_state(BotState.lang)
    await message.answer(text=_('Iltimos, tilni tanlang'), reply_markup=language_button())


@main_router.callback_query(BotState.lang, F.data.startswith('lang'))
async def change_language(callback: CallbackQuery, state: FSMContext, i18n: I18n):
    curr = callback.data.split('_')[-1]
    default = callback.from_user.language_code
    if curr:
        await state.update_data({"locale": curr})
        i18n.current_locale = curr
    else:
        await state.update_data({"locale": default})
        i18n.current_locale = default
    await callback.message.answer(_("Til muvoffaqiyatli o'zgartirildi !!!"), reply_markup=role_button())
