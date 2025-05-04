from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _ , lazy_gettext as __

from bot.buttons.inline import gender_button, woman, man, admin_contact, back_t
from bot.buttons.reply import contact_button, back_button, employee_text, employee_main_panel_button, last_name, \
    category, contact_us, settings, employer_main_panel_button, contact, first_name, about_me, back_text, \
    employee_update, gender, work_type, agriculture, construction, household_chores, any_, work_description
from bot.states import EmployeeForm
from db.models import Employee, User, Employer, GenderType

employee_router = Router()

@employee_router.message(EmployeeForm.update_name,F.text == __(back_text))
@employee_router.message(EmployeeForm.update_lname,F.text == __(back_text))
@employee_router.message(EmployeeForm.update_contact,F.text == __(back_text))
@employee_router.message(EmployeeForm.update_gender,F.text == __(back_text))
@employee_router.message(EmployeeForm.update_work_t,F.text == __(back_text))
@employee_router.message(EmployeeForm.update_work_d,F.text == __(back_text))
@employee_router.message(EmployeeForm.gender,F.data == back_t)
@employee_router.message(EmployeeForm.work_type,F.text == __(back_text))
@employee_router.message(EmployeeForm.work_description,F.text == __(back_text))
@employee_router.message(EmployeeForm.last_name,F.text == __(back_text))
@employee_router.message(EmployeeForm.settings,F.text == __(back_text))
@employee_router.message(EmployeeForm.about_me,F.text == __(back_text))
@employee_router.message(F.text == __(employee_text))
async def name_handler(message:Message, state:FSMContext):
    user_id = message.from_user.id
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


@employee_router.callback_query(EmployeeForm.gender, F.data.in_(["man", "woman"]))
async def work_type_handler(callback:CallbackQuery, state:FSMContext):
    gender = GenderType(callback.data)
    await state.update_data({'gender':gender})
    await state.set_state(EmployeeForm.work_type)
    await callback.message.answer(_("Nima ish qilasiz?"), reply_markup=category())


@employee_router.message(EmployeeForm.work_type,F.text.in_([__(agriculture),__(construction),__(household_chores), __(any_)]))
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
    await state.set_state(EmployeeForm.phone_number)
    await message.answer(_("Telefon raqamingizni pastdagi tugmani bosish orqali yuboring:"),
                         reply_markup=contact_button())


@employee_router.message(EmployeeForm.phone_number, F.contact)
async def save_employee(message:Message, state:FSMContext):
    phone_number = message.contact.phone_number
    chat_id = message.from_user.id
    user = await User.get(chat_id)
    if user:
        data = await state.get_data()
        username = message.from_user.username
        await Employee.create(
            chat_id=chat_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=phone_number,
            username=username,
            gender = data.get("gender"),
            work_type=data.get("work_type"),
            work_description=data.get("work_description")
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
            "Ism: {first_name}\nFamiliya: {last_name}\nJinsi: {gender}\nTelefon raqam: {phone_number}"
        ).format(first_name=employee.first_name, last_name=employee.last_name ,
                 phone_number=employee.phone_number,gender=employee.gender.value)
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
                                                            __(contact), __(gender), __(work_type), __(work_description)]))
async def update_user(message: Message,state:FSMContext):
    if message.text == __(first_name):
        await state.set_state(EmployeeForm.update_name)
        await message.answer(text=_('Iltimos, ismingizni kiriting:'), reply_markup=back_button())
    elif message.text == __(contact):
        await state.set_state(EmployeeForm.update_contact)
        await message.answer(text=_("Iltimos, telefon raqam kiriting:"), reply_markup=back_button())
    elif message.text == __(last_name):
        await state.set_state(EmployeeForm.update_lname)
        await message.answer(text=_('Iltimos, familiyangizni kiriting:'), reply_markup=back_button())
    elif message.text == __(gender):
        await state.set_state(EmployeeForm.update_gender)
        await message.answer(text=_('Iltimos, jinsingizni tanlang:'), reply_markup=gender_button())
    elif message.text == __(work_type):
        await state.set_state(EmployeeForm.update_work_t)
        await message.answer(text=_('Iltimos, yangi ish turini tanlang:'), reply_markup=category())
    elif message.text == __(work_description):
        await state.set_state(EmployeeForm.update_work_d)
        await message.answer(text=_("Iltimos, nimalar qila olishingiz haqida batafsil ma'lumot bering:"), reply_markup=category())

@employee_router.message(EmployeeForm.update_name, F.text.isalpha())
async def name_updater(message:Message):
    chat_id =  message.from_user.id
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    if user:
        id_ = user.id
        await Employee.update(id_=id_,first_name=message.text)
        await message.answer(_("Ismingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())

@employee_router.message(EmployeeForm.update_lname, F.text.isalpha())
async def surname_updater(message:Message):
    chat_id =  message.from_user.id
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    if user:
        id_ = user.id
        await Employee.update(id_=id_,last_name=message.text)
        await message.answer(_("Familiyangiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())

@employee_router.message(EmployeeForm.update_contact, F.text.isdigit())
async def contact_updater(message:Message):
    chat_id =  message.from_user.id
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    if user:
        id_=user.id
        await Employee.update(id_=id_,contact=message.text)
        await message.answer(_("Telefon raqamingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())

@employee_router.callback_query(EmployeeForm.update_gender, F.text.in_(["man", "woman"]))
async def gender_updater(callback:CallbackQuery):
    chat_id =  callback.from_user.id
    gender = GenderType(callback.data)
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    if user:
        id_=user.id
        await Employee.update(id_=id_,gender=gender)
        await callback.message.answer(_("Jinsingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())

@employee_router.message(EmployeeForm.update_work_t,F.text.in_([__(agriculture),__(construction),__(household_chores), __(any_)]))
async def contact_updater(message:Message):
    chat_id =  message.from_user.id
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    if user:
        id_ = user.id
        await Employee.update(id_=id_,work_type=message.text)
        await message.answer(_("Ish turi muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())

@employee_router.message(EmployeeForm.update_work_d, F.text)
async def contact_updater(message:Message):
    chat_id =  message.from_user.id
    user = await Employee.get_by_chat_id(chat_id=chat_id)
    if user:
        id_ = user.id
        await Employee.update(id_=id_,work_description=message.text)
        await message.answer(_("Ma'lumot muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())
