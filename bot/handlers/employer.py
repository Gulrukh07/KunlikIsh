from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _ , lazy_gettext as __

from bot.buttons.inline import admin_contact
from bot.buttons.reply import employer_text, employer_main_panel_button, back_button, back_text, contact_button, \
    about_me, contact_us, settings, employer_update, first_name, last_name, contact, my_orders, order_now
from bot.states import EmployerForm, WorkForm
from db.models import Employer, User

employer_router = Router()


@employer_router.message(WorkForm.workers, F.text == __(back_text))
@employer_router.message(WorkForm.gender, F.text == __(back_text))
@employer_router.message(WorkForm.description, F.text == __(back_text))
@employer_router.message(WorkForm.price, F.text == __(back_text))
@employer_router.message(WorkForm.photo, F.text == __(back_text))
@employer_router.message(WorkForm.location, F.text == __(back_text))
@employer_router.message(WorkForm.gender, F.text == __(back_text))
@employer_router.message(EmployerForm.update_name, F.text == __(back_text))
@employer_router.message(EmployerForm.update_lname, F.text == __(back_text))
@employer_router.message(EmployerForm.update_contact, F.text == __(back_text))
@employer_router.message(EmployerForm.about_me, F.text == __(back_text))
@employer_router.message(EmployerForm.settings, F.text == __(back_text))
@employer_router.message(EmployerForm.main_panel, F.text == __(back_text))
@employer_router.message(EmployerForm.phone_number,F.text == __(back_text))
@employer_router.message(F.text == __(employer_text))
async def name_handler(message:Message, state:FSMContext):
    user_id = message.from_user.id
    employer = await Employer.get_by_chat_id(chat_id=user_id)
    if not employer:
        await state.set_state(EmployerForm.first_name)
        await message.answer(_('Ismingizni Kiriting:'))
    else:
        await state.set_state(EmployerForm.main_panel)
        await message.answer(_('🏠Asosiy Menyuga xush kelibsiz'), reply_markup=employer_main_panel_button())


@employer_router.message(EmployerForm.first_name,F.text.isalpha())
async def surname_handler(message:Message, state:FSMContext):
    first_name = message.text
    await state.update_data({'first_name':first_name})
    await state.set_state(EmployerForm.last_name)
    await message.answer(_("Familiyangizni kiriting:"), reply_markup=back_button())


@employer_router.message(EmployerForm.last_name,F.text.isalpha())
async def contact_handler(message:Message, state:FSMContext):
    last_name = message.text
    await state.update_data({'last_name':last_name})
    await state.set_state(EmployerForm.phone_number)
    await message.answer(_("Telefon raqamingizni pastdagi tugmani bosish orqali yuboring:"),
                         reply_markup=contact_button())

@employer_router.message(EmployerForm.phone_number, F.contact)
async def save_employer(message:Message, state:FSMContext):
    phone_number = message.contact.phone_number
    chat_id = message.from_user.id
    data = await state.get_data()
    username = message.from_user.username
    user = await User.get(chat_id)
    if user:
        await Employer.create(
            chat_id=chat_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=phone_number,
            username=username
        )
    await state.set_state(EmployerForm.main_panel)
    await message.answer(_("🏠Asosiy menyuga xush kelibsiz!"), reply_markup=employer_main_panel_button())


@employer_router.message(EmployerForm.main_panel, F.text == __(about_me))
async def about_me(message:Message, state:FSMContext):
    chat_id =message.from_user.id
    employer = await Employer.get_by_chat_id(chat_id=chat_id)
    await state.set_state(EmployerForm.about_me)
    if employer:
        about_me = _(
            "Ism: {first_name}\nFamiliya: {last_name}\nTelephon raqam: {phone_number}\n"
        ).format(first_name=employer.first_name, last_name=employer.last_name ,phone_number=employer.phone_number)
    else:
        about_me = _("Ma'lumot topilmadi!")
    await message.answer(text=about_me, reply_markup=back_button())

@employer_router.message(EmployerForm.main_panel, F.text == __(contact_us))
async def contact_us(message:Message):
    await message.answer(_("Admin bilan bog'lanish"), reply_markup=admin_contact())


@employer_router.message(EmployerForm.main_panel, F.text == __(settings))
async def settings_handler(message:Message, state:FSMContext):
    chat_id =message.from_user.id
    employer = await Employer.get_by_chat_id(chat_id=chat_id)
    await state.set_state(EmployerForm.settings)
    await message.answer(text=_("Bu yerda siz ma'lumotlaringizni o'zgartira olasiz!!"))
    if employer:
        await message.answer(_("Nimani o'zgartirmoqchisiz?"), reply_markup=employer_update())
    else:
        await message.answer(_("Ma'lumot topilmadi!"), reply_markup=back_button())

@employer_router.message(EmployerForm.settings, F.text.in_((__(first_name), __(last_name), __(contact))))
async def update_user(message: Message, state:FSMContext):
    if message.text == __(first_name):
        await state.set_state(EmployerForm.update_name)
        await message.answer(text=_('Iltimos, ismingizni kiriting:'), reply_markup=back_button())
    elif message.text == __(contact):
        await state.set_state(EmployerForm.update_contact)
        await message.answer(text=_("Iltimos, telefon raqamni + belgisisiz kiriting:"), reply_markup=back_button())
    elif message.text == __(last_name):
        await state.set_state(EmployerForm.update_lname)
        await message.answer(text=_('Iltimos, familiyangizni kiriting:'), reply_markup=back_button())

@employer_router.message(EmployerForm.update_name, F.text.isalpha())
async def name_updater(message:Message):
    chat_id =  message.from_user.id
    user = await Employer.get_by_chat_id(chat_id=chat_id)
    if user:
        id_ = user.id
        await Employer.update(id_=id_,first_name=message.text)
        await message.answer(_("Ismingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())

@employer_router.message(EmployerForm.update_lname, F.text.isalpha())
async def surname_updater(message:Message):
    chat_id =  message.from_user.id
    user = await Employer.get_by_chat_id(chat_id=chat_id)
    if user:
        id_ = user.id
        await Employer.update(id_=id_, last_name=message.text)
        await message.answer(_("Familiyangiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())

@employer_router.message(EmployerForm.update_contact, F.text.isdigit())
async def contact_updater(message:Message):
    chat_id =  message.from_user.id
    user = await Employer.get_by_chat_id(chat_id=chat_id)
    if user:
        id_ = user.id
        await Employer.update(id_=id_, phone_number=message.text)
        await message.answer(_("Telefon raqamingiz muvaffaqiyatli o'zgartirildi!"), reply_markup=back_button())

@employer_router.message(EmployerForm.main_panel, F.text == __(my_orders))
async def orders(message:Message):
    employer = await Employer.get_by_chat_id(message.from_user.id)
    if employer:
        works = employer.works
        data = []
        for i, work in enumerate( works, start=1):
            created_at = work.created_at
            formatted_date = created_at.strftime("%Y-%m-%d")
            data.append(
                _("""Sizning {i} - buyurtmangiz: \n\n
                📌 Nomi: {title}\n
                📝 Ish tavsiloti: {description}\n
                💰 Narxi: {price}\n
                📅 Buyurtma sanasi: {created_at}
                """).format(i=i, title=work.title, description = work.description,
                            price=work.price,created_at = formatted_date)
            )
        formatted_data = "\n" + "\n".join(data)
        await message.answer(text=_('Sizning Buyurtmalaringiz:{}').format(formatted_data), reply_markup=back_button())


