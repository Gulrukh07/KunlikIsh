from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _ , lazy_gettext as __

from bot.buttons.inline import gender_button, woman, man, admin_contact, back_t
from bot.buttons.reply import contact_button, back_button, employee_text, employee_main_panel_button, last_name, \
    category, contact_us, settings, employer_main_panel_button, contact, first_name, about_me, back_text, back_to_start, \
    employee_update, gender, work_type, agriculture, construction, household_chores, any_
from bot.states import EmployeeForm
from db.models import Employee

employee_router = Router()

@employee_router.message(EmployeeForm.gender,F.data == back_t)
@employee_router.message(EmployeeForm.work_type,F.text == __(back_text))
@employee_router.message(EmployeeForm.work_description,F.text == __(back_text))
@employee_router.message(EmployeeForm.last_name,F.text == __(back_text))
@employee_router.message(EmployeeForm.settings,F.text == __(back_text))
@employee_router.message(EmployeeForm.about_me,F.text == __(back_text))
@employee_router.message(F.text == __(employee_text))
async def name_handler(message:Message, state:FSMContext):
    user_id = str(message.from_user.id)
    employee = await Employee.get_by_chat_id(chat_id=user_id)
    if not employee:
        await state.set_state(EmployeeForm.first_name)
        await message.answer(_('Ismingizni Kiriting:'))
    else:
        await state.set_state(EmployeeForm.main_panel)
        await message.answer(_('🏠Asosiy Menyuga xush kelibsiz'), reply_markup=employee_main_panel_button())


@employee_router.message(EmployeeForm.first_name,F.text.isalpha())
async def surname_handler(message:Message, state:FSMContext):
    first_name = message.text
    await state.update_data({'first_name':first_name})
    await state.set_state(EmployeeForm.last_name)
    await message.answer(_("Familiyangizni kiriting:"), reply_markup=back_button())


@employee_router.message(EmployeeForm.last_name,F.text.isalpha())
async def gender_handler(message:Message, state:FSMContext):
    last_name = message.text
    await state.update_data({'last_name':last_name})
    await state.set_state(EmployeeForm.gender)
    await message.answer(_("Jinsingiz:"), reply_markup=gender_button())


@employee_router.message(EmployeeForm.gender,F.text.in_([man, woman]))
async def work_type_handler(message:Message, state:FSMContext):
    gender = message.text
    await state.update_data({'gender':gender})
    await state.set_state(EmployeeForm.work_type)
    await message.answer(_("Nima ish qilasiz?"), reply_markup=category())


@employee_router.message(EmployeeForm.work_type,F.text.in_([agriculture,construction,household_chores, any_]))
async def work_type_handler(message:Message, state:FSMContext):
    work_type = message.text
    await state.update_data({'work_type':work_type})
    await state.set_state(EmployeeForm.work_description)
    await message.answer(_("Iltimos, nima ishlar qila olishingiz haqida batafsil ma'lumot bering"),
                         reply_markup=back_button())


@employee_router.message(EmployeeForm.work_description,F.text)
async def contact_handler(message:Message, state:FSMContext):
    work_description = message.text
    await state.update_data({'work_description': work_description})
    await message.answer(_("Telefon raqamingizni pastdagi tugmani bosish orqali yuboring:"),
                         reply_markup=contact_button())

    phone_number = message.contact.phone_number
    data = await state.get_data()
    username = message.from_user.username
    await Employee.create(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        phone_number=phone_number,
        username=username
    )

    await state.set_state(EmployeeForm.main_panel)
    await message.answer(_("🏠Asosiy menyuga xush kelibsiz!"), reply_markup=employee_main_panel_button())


@employee_router.message(EmployeeForm.main_panel, F.text == __(about_me))
async def about_me(message:Message, state:FSMContext):
    chat_id =message.from_user.id
    employee = await Employee.get_by_chat_id(chat_id=chat_id)
    await state.set_state(EmployeeForm.about_me)
    if employee:
        about_me = _(
            "Ism: {first_name}\nFamiliya: {last_name}\nJinsi: {gender}\nTelephon raqam: {phone_number}"
        ).format(first_name=employee.first_name, last_name=employee.last_name ,
                 phone_number=employee.phone_number,gender=employee.gender)
    else:
        about_me = _("Ma'lumot topilmadi")
    await message.answer(text=about_me, reply_markup=back_button())

@employee_router.message(EmployeeForm.main_panel, F.text == __(contact_us))
async def contact_us(message:Message):
    await message.answer(_("Admin bilan bog'lanish"), reply_markup=admin_contact())


@employee_router.message(EmployeeForm.main_panel, F.text == __(settings))
async def settings_handler(message:Message, state:FSMContext):
    chat_id =message.from_user.id
    employee = await Employee.get_by_chat_id(chat_id=chat_id)
    await state.set_state(EmployeeForm.settings)
    await message.answer(text=_("Bu yerda siz ma'lumotlaringizni o'zgartira olasiz!!"))
    if employee:
        await message.answer(_("Nimani o'zgartirmoqchisiz?"), reply_markup=employee_update())
    else:
        await message.answer(_("Ma'lumot topilmadi!"), reply_markup=back_button())

@employee_router.message(EmployeeForm.settings, F.text.in_([__(first_name), __(last_name),
                                                            __(contact), __(gender), __(work_type)]))
async def update_user(message: Message):
    if message.text == __(first_name):
        await message.answer(text=_('Iltimos, ismingizni kiriting:'), reply_markup=back_button())
    elif message.text == __(contact):
        await message.answer(text=_("Iltimos, telefon raqam kiriting:"), reply_markup=back_button())
    elif message.text == __(last_name):
        await message.answer(text=_('Iltimos, familiyangizni kiriting:'), reply_markup=back_button())
    elif message.text == __(gender):
        await message.answer(text=_('Iltimos, jinsingizni tanlang:'), reply_markup=gender_button())
    elif message.text == __(last_name):
        await message.answer(text=_('Iltimos, yangi ish turini tanlang:'), reply_markup=category())

@employee_router.message(EmployeeForm.settings, F.text == __(first_name))
async def name_updater(message:Message):
    chat_id =  str(message.from_user.id)
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    user.update(first_name=message.text)
    await message.answer(_("Ismingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=employer_main_panel_button())

@employee_router.message(EmployeeForm.settings, F.text == __(last_name))
async def surname_updater(message:Message):
    chat_id =  str(message.from_user.id)
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    user.update(last_name=message.text)
    await message.answer(_("Familiyangiz muvaffaqiyatli o'zgartirildi!"), reply_markup=employee_main_panel_button())

@employee_router.message(EmployeeForm.settings, F.text == __(contact))
async def contact_updater(message:Message):
    chat_id =  str(message.from_user.id)
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    user.update(contact=message.text)
    await message.answer(_("Telefon raqamingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=employee_main_panel_button())

@employee_router.callback_query(EmployeeForm.settings, F.text == __(gender))
async def gender_updater(callback:CallbackQuery):
    chat_id =  str(callback.from_user.id)
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    user.update(gender=callback.data)
    await callback.message.answer(_("Jinsingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=employee_main_panel_button())

@employee_router.message(EmployeeForm.settings, F.text == __(work_type))
async def contact_updater(message:Message):
    chat_id =  str(message.from_user.id)
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    user.update(work_type=message.text)
    await message.answer(_("Ish turi muvaffaqiyatli o'zgartirildi!"), reply_markup=employee_main_panel_button())
