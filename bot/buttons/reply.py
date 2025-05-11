from aiogram.types import KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_reply_button(buttons: list, sizes: list, repeat=False):
    rkb = ReplyKeyboardBuilder()
    rkb.add(*buttons)
    if repeat:
        rkb.adjust(sizes[0], repeat=True)
    else:
        rkb.adjust(*sizes)
    return rkb.as_markup(resize_keyboard=True)


def back_button():
    btn = [KeyboardButton(text=_('️Orqaga'))]
    size = [1]
    return make_reply_button(buttons=btn, sizes=size)


def role_button():
    buttons = [
        KeyboardButton(text=_('Ish beruvchi')),
        KeyboardButton(text=_('Ishchi')),
    ]
    size = [2]
    return make_reply_button(buttons=buttons, sizes=size)


def employer_main_panel_button():
    buttons = [
        KeyboardButton(text=_('Hozi buyurtma berish')),
        KeyboardButton(text=_("Menin buyurtmalarim")),
        KeyboardButton(text=_('Sozlamalar')),
        KeyboardButton(text=_('Men haqimda')),
        KeyboardButton(text=_("Biz bilan bog'lanish")),
        KeyboardButton(text=_('Startga qaytish')),
    ]
    sizes = [2]
    return make_reply_button(buttons=buttons, sizes=sizes, repeat=True)


def contact_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text=_('Contact'), request_contact=True),
        KeyboardButton(text=_('️Back'))
    ])
    rkb.adjust(2)
    return rkb.as_markup(resize_keyboard=True)


def employer_update():
    buttons = [
        KeyboardButton(text=_('Ish')),
        KeyboardButton(text=_('Familiya')),
        KeyboardButton(text=_('Telefon raqam')),
        KeyboardButton(text=_('️Orqaga')),
    ]
    sizes = [2]
    return make_reply_button(buttons=buttons, sizes=sizes, repeat=True)


def employee_update():
    buttons = [
        KeyboardButton(text=_('Ish')),
        KeyboardButton(text=_('Familiya')),
        KeyboardButton(text=_('Telefon raqam')),
        KeyboardButton(text=_('Jins')),
        KeyboardButton(text=_('Ish turi')),
        KeyboardButton(text=_('Ish haqida')),
        KeyboardButton(text=_('️Orqaga')),
    ]
    sizes = [2]
    return make_reply_button(buttons=buttons, sizes=sizes, repeat=True)


def category():
    buttons = [
        KeyboardButton(text=_("Qishloq Xo'jaligi")),
        KeyboardButton(text=_("Qurilish Ishlari")),
        KeyboardButton(text=_("Uy ishlari")),
        KeyboardButton(text=_("Har qanday")),
        KeyboardButton(text=_('️Orqaga')),
    ]
    sizes = [2]
    return make_reply_button(buttons=buttons, sizes=sizes, repeat=True)


def employee_main_panel_button():
    buttons = [
        KeyboardButton(text=_('Men haqimda')),
        KeyboardButton(text=_('Sozlamalar')),
        KeyboardButton(text=_("Biz bilan bog'lanish")),
        KeyboardButton(text=_("Mening reytingim")),
        KeyboardButton(text=_('Startga qaytish')),
    ]
    sizes = [2]
    return make_reply_button(buttons=buttons, sizes=sizes, repeat=True)


def send_admin():
    buttons = [
        KeyboardButton(text=_("Ha")),
        KeyboardButton(text=_("Yo'q")),
    ]
    sizes = [2]
    return make_reply_button(buttons, sizes)


def rating():
    btns = [
        KeyboardButton(text="5"),
        KeyboardButton(text="4"),
        KeyboardButton(text="3"),
        KeyboardButton(text="2"),
        KeyboardButton(text="1"),
    ]
    sizes = [1, 2, 2]
    return make_reply_button(buttons=btns, sizes=sizes)
