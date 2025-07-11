from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram_media_group import media_group_handler

from bot.buttons.inline import gender_button
from bot.buttons.reply import employer_main_panel_button, category, back_button, send_admin
from bot.states import EmployerForm, WorkForm
from db.models import Category, Work, GenderType, Photo, Employer

work_router = Router()


@work_router.message(EmployerForm.main_panel, F.text == __('Hozir buyurtma berish'))
async def order_now_handler(message: Message, state: FSMContext):
    await state.set_state(WorkForm.title)
    await message.answer(_("Itimos, Ish haqida Ma'lumot Bering!"))
    await message.answer(_("Ishning nomi:"), reply_markup=ReplyKeyboardRemove())


@work_router.message(WorkForm.title, F.text.isalpha())
async def order_now_handler(message: Message, state: FSMContext):
    await state.update_data({"title": message.text})
    await state.set_state(WorkForm.category)
    await message.answer(_("Iltimos Ish turini tanlang:"), reply_markup=category())


@work_router.message(WorkForm.category,
                     F.text.in_([__("Qishloq Xo'jaligi"), __("Qurilish Ishlari"), __("Uy ishlari"), __("Har qanday")]))
async def order_now_handler(message: Message, state: FSMContext):
    CATEGORY_TRANSLATIONS = {
    "Qurilish Ishlari": "Qurilish Ishlari",
    "Строительные работы": "Qurilish Ishlari",

    "Qishloq Xo'jaligi": "Qishloq Xo'jaligi",
    "Сельское хозяйство": "Qishloq Xo'jaligi",

    "Uy ishlari": "Uy ishlari",
    "Домашние работы": "Uy ishlari",

    "Har qanday": "Har qanday",
    "Любая": "Har qanday",
    }

    category_ = message.text
    mapped_title = CATEGORY_TRANSLATIONS.get(category_)
    c = await Category.get_by_title(title_=mapped_title)
    if c:
        category_id = c.id
        await state.update_data({"category_id": category_id})
        await state.set_state(WorkForm.description)
        await message.answer(_("Iltimos, ish haqida batafsil ma'lumot bering"), reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(_('Bunday tur mavjud emas!\nIltimos, faqat tugmalardan birini tanlang'),
                             reply_markup=category())


@work_router.message(WorkForm.description, F.text)
async def price_handler(message: Message, state: FSMContext):
    await state.update_data({"description": message.text})
    await state.set_state(WorkForm.price)
    await message.answer(_("Qancha To'lov qilmoqchisiz[so'm]?"))


@work_router.message(WorkForm.price, F.text.isdigit())
async def photo_handler(message: Message, state: FSMContext):
    await state.update_data({"price": message.text})
    await state.set_state(WorkForm.photo)
    await message.answer(_("Iltimos, ish joyini rasmlarini yuboring:"))


@work_router.message(F.media_group_id, F.photo)
@media_group_handler
async def handle_media_group_photos(messages: list[Message], state: FSMContext):
    photos = []

    for message in messages:
        file_id = message.photo[-1].file_id
        photos.append(file_id)
        await Photo.create(photo_id=file_id)

    await state.update_data(photos=photos)
    await state.set_state(WorkForm.location)

    await messages[-1].answer(
        _("Iltimos, ish joyini joylashuvini xaritadan tanlab yuboring:"),
        reply_markup=back_button()
    )


@work_router.message(WorkForm.photo, F.photo, ~F.media_group_id)
async def handle_single_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await Photo.create(photo_id=file_id)
    await state.update_data(photos=[file_id])
    await state.set_state(WorkForm.location)
    await message.answer(
        _("Iltimos, ish joyini joylashuvini xaritadan tanlab yuboring:")
    )


@work_router.message(WorkForm.location, F.location)
async def location_handler(message: Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await state.update_data({"latitude": latitude, "longitude": longitude})
    await state.set_state(WorkForm.gender)
    await message.answer(_("Siz kimni qidirayapsiz?"), reply_markup=gender_button())


@work_router.callback_query(WorkForm.gender, F.data.in_(["man", "woman"]))
async def gender_handler(callback: CallbackQuery, state: FSMContext):
    gender = GenderType(callback.data)
    await state.update_data({"worker_gender": gender})
    await state.set_state(WorkForm.workers)
    await callback.message.answer(_("Sizga nechta ishchi kerak?"))


@work_router.message(WorkForm.workers, F.text.isdigit())
async def save_work(message: Message, state: FSMContext):
    number = int(message.text)
    employer_id = message.from_user.id
    data = await state.get_data()
    employer = await Employer.get(telegram_id_=employer_id)
    if employer:
        e_id = employer.id
        work = await Work.create(
            title=data['title'],
            category_id=data['category_id'],
            price=data['price'],
            description=data['description'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            worker_gender=data['worker_gender'],
            num_of_workers=number,
            employer_id=e_id
        )
        photo_ids = data.get("photos", [])
        for photo_id in photo_ids:
            photo = await Photo.get_by_photo_id(photo_id=photo_id)
            if photo:
                id_ = photo.id
                work_id = work.id
                await Photo.update(_id=id_, work_id=work_id)

    await state.update_data(num_of_workers=number)
    await state.update_data(employer_id=employer.id)
    await state.set_state(WorkForm.admin)
    await message.answer(_("Sizning buyurtmangiz adminga yuborilsinmi?"),
                         reply_markup=send_admin())

