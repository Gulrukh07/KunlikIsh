from aiogram.types import InlineKeyboardButton
from aiogram.utils.i18n import gettext as _ , lazy_gettext as __
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons.reply import back_text

language_text = "Language"
uzb_text = "🇺🇿Uzbek"
ru_text = "🇷🇺Russian"
main_panel_text = "🏠Asosiy Menu"
woman = "Ayol"
man = "Erkak"
back_t = '⬅️Orqaga'

def make_inline_button(buttons: list, sizes: list, repeat = False):
    ikb = InlineKeyboardBuilder()
    ikb.add(*buttons)
    if repeat:
        ikb.adjust(sizes[0], repeat=True)
    else:
        ikb.adjust(*sizes)
    return ikb.as_markup()

def language_button():
    btn1 = InlineKeyboardButton(text=uzb_text,callback_data='uz')
    btn2 = InlineKeyboardButton(text=ru_text, callback_data='ru')
    btn3 = InlineKeyboardButton(text=_(main_panel_text),callback_data='main panel')
    buttons = [btn1 , btn2 , btn3]
    size = [2,1]
    return make_inline_button(buttons, size)

def admin_contact():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='Admin', url='https://t.me/KhalilovnaG')])
    ikb.adjust(1)
    return ikb.as_markup(resize_keyboard=True)


def gender_button():
    btn1 = InlineKeyboardButton(text=_(woman), callback_data='woman')
    btn2 = InlineKeyboardButton(text=_(man), callback_data='man')

    buttons = [btn1,btn2]
    size = [2]
    return make_inline_button(buttons=buttons,sizes=size)