from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, I18n

from bot.buttons.inline import language_button
from bot.states import BotState

lang_router = Router()


@lang_router.message(Command('language'))
async def language(message: Message, state: FSMContext):
    await state.set_state(BotState.lang)
    await message.answer(text=_('Iltimos, tilni tanlang'), reply_markup=language_button())


@lang_router.callback_query(BotState.lang, F.data.startswith('lang'))
async def change_language(callback: CallbackQuery, state: FSMContext, i18n: I18n):
    curr = callback.data.split('_')[-1]
    default = callback.from_user.language_code
    if curr:
        await state.set_data({"locale": curr})
        i18n.current_locale = curr
    else:
        await state.set_data({"locale": default})
        i18n.current_locale = default
    await callback.message.answer(_("Current language changed successfully"))
