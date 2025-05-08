# from aiogram import Router
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message
#
# from bot.buttons.inline import language_button
#
# lang_router = Router()
#
#
# @lang_router.message(Command('language'))
# async def language(message: Message, state: FSMContext):
#     await state.set_state(BotState.language)
#     await message.answer(text='Iltimos, tilni tanlang\n'
#                               'Пожалуйста, выберите язык', reply_markup=language_button())
