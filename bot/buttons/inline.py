from aiogram.types import InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_inline_button(buttons: list, sizes: list, repeat=False):
    ikb = InlineKeyboardBuilder()
    ikb.add(*buttons)
    if repeat:
        ikb.adjust(sizes[0], repeat=True)
    else:
        ikb.adjust(*sizes)
    return ikb.as_markup()


def language_button():
    btn1 = InlineKeyboardButton(text=_('🇺🇿Uzbek'), callback_data=f'lang_uz')
    btn2 = InlineKeyboardButton(text=_('🇷🇺Russian'), callback_data=f'lang_ru')
    buttons = [btn1, btn2]
    size = [2]
    return make_inline_button(buttons, size)


def admin_contact():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='Admin', url='https://t.me/KhalilovnaG')])
    ikb.adjust(1)
    return ikb.as_markup(resize_keyboard=True)


def gender_button():
    btn1 = InlineKeyboardButton(text=_('Ayol'), callback_data='woman')
    btn2 = InlineKeyboardButton(text=_('Erkak'), callback_data='man')

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
    btn = [InlineKeyboardButton(text=_('Qabul qilish'), callback_data=f"accepted_{employer_id}_{work_id}")]
    return make_inline_button(btn, sizes=[1])


def chat_with_employee(employee_username):
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=_("Bog'lanish"), url=f"https://t.me/{employee_username}"))
    ikb.adjust(1)
    return ikb.as_markup(resize_keyboard=True)


def deal_button(employee_id, employer_id):
    btn = InlineKeyboardButton(text=_('Kelishildi'), callback_data=f"deal/{str(employee_id)}/{str(employer_id)}")
    return make_inline_button([btn], sizes=[1])
