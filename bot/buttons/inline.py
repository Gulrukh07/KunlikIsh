from aiogram.types import InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

language_text = "Language"
uzb_text = "🇺🇿Uzbek"
ru_text = "🇷🇺Russian"
main_panel_text = "🏠Asosiy Menu"
woman = "Ayol"
man = "Erkak"
back_t = '⬅️Orqaga'
employee_res_text = "Qabul qilish"
deal_text = "Kelishildi"


def make_inline_button(buttons: list, sizes: list, repeat=False):
    ikb = InlineKeyboardBuilder()
    ikb.add(*buttons)
    if repeat:
        ikb.adjust(sizes[0], repeat=True)
    else:
        ikb.adjust(*sizes)
    return ikb.as_markup()


def language_button():
    btn1 = InlineKeyboardButton(text=uzb_text, callback_data='uz')
    btn2 = InlineKeyboardButton(text=ru_text, callback_data='ru')
    btn3 = InlineKeyboardButton(text=_(main_panel_text), callback_data='main panel')
    buttons = [btn1, btn2, btn3]
    size = [2, 1]
    return make_inline_button(buttons, size)


def admin_contact():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='Admin', url='https://t.me/KhalilovnaG')])
    ikb.adjust(1)
    return ikb.as_markup(resize_keyboard=True)


def gender_button():
    btn1 = InlineKeyboardButton(text=_(woman), callback_data='woman')
    btn2 = InlineKeyboardButton(text=_(man), callback_data='man')

    buttons = [btn1, btn2]
    size = [2]
    return make_inline_button(buttons=buttons, sizes=size)


def for_admin():
    btn1 = InlineKeyboardButton(text="✅", callback_data="successfully")
    btn2 = InlineKeyboardButton(text="❌", callback_data="rejected")

    btns = [btn1, btn2]
    sizes = [2]
    return make_inline_button(buttons=btns, sizes=sizes)


def employee_response(employer_id, work_id):
    btn = [InlineKeyboardButton(text=_(employee_res_text), callback_data=f"accepted_{employer_id}_{work_id}")]
    return make_inline_button(btn, sizes=[1])


def chat_with_employee(employee_username):
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=_("Bog'lanish"), url=f"https://t.me/{employee_username}"))
    ikb.adjust(1)
    return ikb.as_markup(resize_keyboard=True)


def deal_button(employee_id, employer_id):
    btn = InlineKeyboardButton(text=_(deal_text), callback_data=f"deal/{str(employee_id)}/{str(employer_id)}")
    return make_inline_button([btn], sizes=[1])
