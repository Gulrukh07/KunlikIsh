from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.inline import gender_button, admin_contact
from bot.buttons.reply import back_button, category, employee_main_panel_button, contact_button, employee_update
from bot.states import EmployeeForm
from db.models import Employee, User, GenderType, Work, Rating

employee_router = Router()


@employee_router.message(EmployeeForm.rating, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.update_name, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.update_lname, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.update_contact, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.update_gender, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.update_work_t, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.update_work_d, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.gender, F.data == '⬅️Orqaga')
@employee_router.message(EmployeeForm.work_type, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.work_description, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.last_name, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.settings, F.text == __('️Orqaga'))
@employee_router.message(EmployeeForm.about_me, F.text == __('️Orqaga'))
@employee_router.message(F.text == __('Ishchi'))
async def name_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    employee = await Employee.get(telegram_id_=user_id)
    if not employee:
        await state.set_state(EmployeeForm.first_name)
        await message.answer(_('Ismingizni Kiriting:'), reply_markup=ReplyKeyboardRemove())
    else:
        await state.set_state(EmployeeForm.main_panel)
        await message.answer(_('🏠Asosiy Menyuga xush kelibsiz'), reply_markup=employee_main_panel_button())


@employee_router.message(EmployeeForm.first_name, F.text.isalpha())
async def surname_handler(message: Message, state: FSMContext):
    first_name = message.text
    await state.update_data({'first_name': first_name})
    await state.set_state(EmployeeForm.last_name)
    await message.answer(_("Familiyangizni kiriting:"), reply_markup=back_button())


@employee_router.message(EmployeeForm.last_name, F.text.isalpha())
async def gender_handler(message: Message, state: FSMContext):
    last_name = message.text
    await state.update_data({'last_name': last_name})
    await state.set_state(EmployeeForm.gender)
    await message.answer(_("Jinsingiz:"), reply_markup=gender_button())


@employee_router.callback_query(EmployeeForm.gender, F.data.in_(["man", "woman"]))
async def work_type_handler(callback: CallbackQuery, state: FSMContext):
    gender = GenderType(callback.data)
    await state.update_data({'gender': gender})
    await state.set_state(EmployeeForm.work_type)
    await callback.message.answer(_("Nima ish qilasiz?"), reply_markup=category())


@employee_router.message(EmployeeForm.work_type,
                         F.text.in_(
                             [__("Qishloq Xo'jaligi"), __("Qurilish Ishlari"), __("Uy ishlari"), __("Har qanday")]))
async def work_type_handler(message: Message, state: FSMContext):
    work_type = message.text
    await state.update_data({'work_type': work_type})
    await state.set_state(EmployeeForm.work_description)
    await message.answer(_("Iltimos, nima ishlar qila olishingiz haqida batafsil ma'lumot bering"),
                         reply_markup=back_button())


@employee_router.message(EmployeeForm.work_description, F.text)
async def contact_handler(message: Message, state: FSMContext):
    work_description = message.text
    await state.update_data({'work_description': work_description})
    await state.set_state(EmployeeForm.phone_number)
    await message.answer(_("Telefon raqamingizni pastdagi tugmani bosish orqali yuboring:"),
                         reply_markup=contact_button())


@employee_router.message(EmployeeForm.phone_number, F.contact)
async def save_employee(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    chat_id = message.from_user.id
    user = await User.get(telegram_id_=chat_id)
    if user:
        data = await state.get_data()
        username = message.from_user.username
        await Employee.create(
            chat_id=chat_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=phone_number,
            username=username,
            gender=data.get("gender"),
            work_type=data.get("work_type"),
            work_description=data.get("work_description")
        )

    await state.set_state(EmployeeForm.main_panel)
    await message.answer(_("🏠Asosiy menyuga xush kelibsiz!"), reply_markup=employee_main_panel_button())


@employee_router.message(EmployeeForm.main_panel, F.text == __('Men haqimda'))
async def about_me(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    employee = await Employee.get(telegram_id_=chat_id)
    await state.set_state(EmployeeForm.about_me)
    if employee:
        about_me = _(
            "Ism: {first_name}\nFamiliya: {last_name}\nJinsi: {gender}\nTelefon raqam: {phone_number}"
        ).format(first_name=employee.first_name, last_name=employee.last_name,
                 phone_number=employee.phone_number, gender=employee.gender.value)
    else:
        about_me = _("Ma'lumot topilmadi")
    await message.answer(text=about_me, reply_markup=back_button())


@employee_router.message(EmployeeForm.main_panel, F.text == __("Biz bilan bog'lanish"))
async def contact_us(message: Message):
    await message.answer(_("Admin bilan bog'lanish"), reply_markup=admin_contact())


@employee_router.message(EmployeeForm.main_panel, F.text == __('Sozlamalar'))
async def settings_handler(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    employee = await Employee.get(telegram_id_=chat_id)
    await state.set_state(EmployeeForm.settings)
    await message.answer(text=_("Bu yerda siz ma'lumotlaringizni o'zgartira olasiz!!"))
    if employee:
        await message.answer(_("Nimani o'zgartirmoqchisiz?"), reply_markup=employee_update())
    else:
        await message.answer(_("Ma'lumot topilmadi!"), reply_markup=back_button())


@employee_router.message(EmployeeForm.settings, F.text.in_([__('Ism'), __('Familiya'),
                                                            __('Telefon raqam'), __('Jins'), __('Ish turi'),
                                                            __('Ish haqida')]))
async def update_user(message: Message, state: FSMContext):
    if message.text == __('Ism'):
        await state.set_state(EmployeeForm.update_name)
        await message.answer(text=_('Iltimos, ismingizni kiriting:'), reply_markup=back_button())
    elif message.text == __('Telefon raqam'):
        await state.set_state(EmployeeForm.update_contact)
        await message.answer(text=_("Iltimos, telefon raqamni + belgisisiz kiriting:"), reply_markup=back_button())
    elif message.text == __('Familiyaangiz'):
        await state.set_state(EmployeeForm.update_lname)
        await message.answer(text=_('Iltimos, familiyangizni kiriting:'), reply_markup=back_button())
    elif message.text == __('Jins'):
        await state.set_state(EmployeeForm.update_gender)
        await message.answer(text=_('Iltimos, jinsingizni tanlang:'), reply_markup=gender_button())
    elif message.text == __('Ish turi'):
        await state.set_state(EmployeeForm.update_work_t)
        await message.answer(text=_('Iltimos, yangi ish turini tanlang:'), reply_markup=category())
    elif message.text == __('Ish haqida'):
        await state.set_state(EmployeeForm.update_work_d)
        await message.answer(text=_("Iltimos, nimalar qila olishingiz haqida batafsil ma'lumot bering:"),
                             reply_markup=category())


@employee_router.message(EmployeeForm.update_name, F.text.isalpha())
async def name_updater(message: Message):
    chat_id = message.from_user.id
    user = await Employee.get(telegram_id_=chat_id)
    if user:
        id_ = user.id
        await Employee.update(_id=id_, first_name=message.text)
        await message.answer(_("Ismingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())


@employee_router.message(EmployeeForm.update_lname, F.text.isalpha())
async def surname_updater(message: Message):
    chat_id = message.from_user.id
    user = await Employee.get(telegram_id_=chat_id)
    if user:
        id_ = user.id
        await Employee.update(_id=id_, last_name=message.text)
        await message.answer(_("Familiyangiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())


@employee_router.message(EmployeeForm.update_contact, F.text.isdigit())
async def contact_updater(message: Message):
    chat_id = message.from_user.id
    user = await Employee.get(telegram_id_=chat_id)
    if user:
        id_ = user.id
        await Employee.update(_id=id_, phone_number=message.text)
        await message.answer(_("Telefon raqamingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())


@employee_router.callback_query(EmployeeForm.update_gender, F.text.in_(["man", "woman"]))
async def gender_updater(callback: CallbackQuery):
    chat_id = callback.from_user.id
    gender = GenderType(callback.data)
    user = await Employee.get(telegram_id_=chat_id)
    if user:
        id_ = user.id
        await Employee.update(_id=id_, gender=gender)
        await callback.message.answer(_("Jinsingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())


@employee_router.message(EmployeeForm.update_work_t, F.text.in_(
    [__("Qishloq Xo'jaligi"), __("Qurilish Ishlari"), __("Uy ishlari"), __("Har qanday")]))
async def contact_updater(message: Message):
    chat_id = message.from_user.id
    user = await Employee.get(telegram_id_=chat_id)
    if user:
        id_ = user.id
        await Employee.update(_id=id_, work_type=message.text)
        await message.answer(_("Ish turi muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())


@employee_router.message(EmployeeForm.update_work_d, F.text)
async def contact_updater(message: Message):
    chat_id = message.from_user.id
    user = await Employee.get(telegram_id_=chat_id)
    if user:
        id_ = user.id
        await Employee.update(_id=id_, work_description=message.text)
        await message.answer(_("Ma'lumot muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())


@employee_router.message(EmployeeForm.main_panel, F.text == __("Mening reytingim"))
async def me_rating(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    # works = (
    #     await session.execute(
    #         select(Work)
    #         .options(selectinload(Work.rating))
    #         .where(Work.employee_id == employee.id)
    #     )
    # ).scalars().all()
    await state.set_state(EmployeeForm.rating)
    employee = await Employee.get(telegram_id_=chat_id)
    works = await Work.filter(employee_id=employee.id)
    data = []
    for i, work in enumerate(works):
        ratings = await Rating.filter(work_id=work.id)
        for rating in ratings:
            data.append(
                _("""Sizning {i} - ishingiz: \n\n
                    📌 Nomi: {title}\n
                    📝 Ish tavsiloti: {description}\n
                    💰 Narxi: {price}\n
                    📅 Buyurtma sanasi: {created_at}\n
                    📊 Reyting: {rating}\n
                    💬 Sharx: {feedback}
                    """).format(i=i, title=work.title, description=work.description,
                                price=work.price, created_at=work.created_at.strftime("%Y-%m-%d"),
                                rating=rating.rating, feedback=rating.feedback),
            )
    formatted_data = "\n" + "\n".join(data)
    await message.answer(text=_('Sizning Reytinglaringiz:{}').format(formatted_data), reply_markup=back_button())
