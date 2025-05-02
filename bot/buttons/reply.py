from aiogram.types import KeyboardButton
from aiogram.utils.i18n import gettext as _ , lazy_gettext as __
from aiogram.utils.keyboard import ReplyKeyboardBuilder

back_text = '⬅️Orqaga'
employer_text = 'Ish beruvchi'
employee_text = 'Ishchi'
back_to_start = 'Startga qaytish'
order_now = 'Hozir buyurtma berish'
my_orders = "Mening buyurtmalarim"
settings = 'Sozlamalar'
about_me = 'Men haqimda'
contact_us = "Biz bilan bog'lanish"
first_name = 'Ism'
gender = 'Jins'
work_type = 'Ish turi'
last_name = 'Familiya'
contact = 'Telefon raqam'
agriculture = "Qishloq Xo'jaligi"
construction = "Qurilish Ishlari"
household_chores = "Uy ishlari"
any_ = "Har qanday"

def make_reply_button(buttons:list, sizes:list, repeat=False):
    rkb = ReplyKeyboardBuilder()
    rkb.add(*buttons)
    if repeat:
        rkb.adjust(sizes[0], repeat=True)
    else:
        rkb.adjust(*sizes)
    return rkb.as_markup(resize_keyboard=True)

def back_button():
    btn = [KeyboardButton(text=_(back_text))]
    size = [1]
    return make_reply_button(buttons=btn, sizes=size)


def role_button():
    btn1 =KeyboardButton(text=_(employer_text))
    btn2 =KeyboardButton(text=_(employee_text))
    btn3 =KeyboardButton(text=_(back_to_start))
    buttons = [btn1, btn2, btn3]
    size = [2,1]
    return make_reply_button(buttons=buttons, sizes=size)


def employer_main_panel_button():
    btn1 = KeyboardButton(text=_(order_now))
    btn2 = KeyboardButton(text=_(my_orders))
    btn3 = KeyboardButton(text=_(settings))
    btn4 =KeyboardButton(text=_(about_me))
    btn5 =KeyboardButton(text=_(contact_us))
    btn6 =KeyboardButton(text=_(back_to_start))

    buttons = [btn1, btn2,btn3,btn4, btn5, btn6]
    sizes = [2]
    make_reply_button(buttons=buttons,sizes=sizes,repeat=True)


def contact_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=_('Contact'), request_contact=True),
              KeyboardButton(text=_('⬅️Back'))])
    rkb.adjust(2)
    return rkb.as_markup(resize_keyboard=True)


def employer_update():
    btn1 = KeyboardButton(text=_(first_name))
    btn2 = KeyboardButton(text=_(last_name))
    btn3 = KeyboardButton(text=_(contact))
    btn4 = KeyboardButton(text=_(back_text))

    buttons = [btn1, btn2,btn3,btn4]
    sizes = [2]
    return make_reply_button(buttons=buttons, sizes=sizes,repeat=True)

def employee_update():
    btn1 = KeyboardButton(text=_(first_name))
    btn2 = KeyboardButton(text=_(last_name))
    btn3 = KeyboardButton(text=_(contact))
    btn4 = KeyboardButton(text=_(gender))
    btn5 = KeyboardButton(text=_(work_type))
    btn6 = KeyboardButton(text=_(back_text))

    buttons = [btn1, btn2,btn3,btn4,btn5,btn6]
    sizes = [2]
    return make_reply_button(buttons=buttons, sizes=sizes,repeat=True)


def category():
    btn1 = KeyboardButton(text=_(agriculture))
    btn2 = KeyboardButton(text=_(construction))
    btn3 = KeyboardButton(text=_(household_chores))
    btn4 = KeyboardButton(text=_(any_))
    btn5 = KeyboardButton(text=_(back_text))

    buttons = [btn1, btn2,btn3,btn4, btn5]
    sizes = [2]
    return make_reply_button(buttons=buttons, sizes=sizes,repeat=True)


def employee_main_panel_button():
    btn1 = KeyboardButton(text=_(about_me))
    btn2 =KeyboardButton(text=_(settings))
    btn3 =KeyboardButton(text=_(contact_us))
    btn4 =KeyboardButton(text=_(back_to_start))

    buttons = [btn1, btn2,btn3,btn4]
    sizes = [2]
    make_reply_button(buttons=buttons,sizes=sizes,repeat=True)

