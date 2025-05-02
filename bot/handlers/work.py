import json

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.inline import gender_button, woman, man
from bot.buttons.reply import order_now, employer_main_panel_button, category, back_button
from bot.states import EmployerForm, WorkForm
from db.models import Category, Work

work_router = Router()

@work_router.message(EmployerForm.main_panel, F.text ==__(order_now))
async def order_now_handler(message:Message, state:FSMContext):
    await state.set_state(WorkForm.title)
    await message.answer(_("Itimos, Ish haqida Ma'lumot Bering!"))
    await message.answer(_("Ishning nomi:"), reply_markup=employer_main_panel_button())

@work_router.message(WorkForm.title, F.text.isalpha())
async def order_now_handler(message:Message, state:FSMContext):
    await state.update_data({"title":message.text})
    await state.set_state(WorkForm.category)
    await message.answer(_("Iltimos Ish turini tanlang:"), reply_markup=category())

@work_router.message(WorkForm.category, F.text)
async def order_now_handler(message:Message, state:FSMContext):
    category_ = message.text
    c = await Category.get_by_title(title_=category_)
    if c:
        category_id = c.id
        await state.update_data({"category_id":category_id})
        await state.set_state(WorkForm.description)
        await message.answer(_("Iltimos, ish haqida batafsil ma'lumot bering"),reply_markup=back_button())
    else:
        await message.answer(_('Bunday tur mavjud emas!\nIltimos, faqat tugmalardan birini tanlang'),
                             reply_markup=category())


@work_router.message(WorkForm.description, F.text)
async def price_handler(message:Message,state:FSMContext):
    await state.update_data({"description":message.text})
    await state.set_state(WorkForm.price)
    await message.answer(_("Qancha To'lov qilmoqchisiz[so'm]?"),reply_markup=back_button())


@work_router.message(WorkForm.description, F.text.isdigit())
async def photo_handler(message:Message,state:FSMContext):
    await state.update_data({"price":message.text})
    await state.set_state(WorkForm.photo)
    await message.answer(_("Iltimos, ish joyini rasmlarini yuboring:"),reply_markup=back_button())


@work_router.message(WorkForm.description, F.photo)
async def photo_handler(message:Message,state:FSMContext):
    file_id = message.photo[0].file_id
    photo_data:dict = await state.get_data()
    with open("photos.json") as f:
        data = json.load(f)
    photo_data['file_id'] = file_id
    data.append(photo_data)
    with open("photos.json" , "w") as f:
        json.dump(data , f ,indent=3)
    await state.update_data({"photo_id":file_id})
    await state.set_state(WorkForm.location)
    await message.answer(_("Iltimos, ish joyini joylashuvini xaritadan tanlab yuboring:"),
                         reply_markup=back_button())


@work_router.message(WorkForm.location, F.location)
async def location_handler(message:Message,state:FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await state.update_data({"latitude":latitude})
    await state.update_data({"longitude":longitude})
    await state.set_state(WorkForm.gender)
    await message.answer(_("Siz kimni qidirayapsiz?"), reply_markup=gender_button())

@work_router.callback_query(WorkForm.gender, F.data.in_([woman, man]))
async def gender_handler(callback:CallbackQuery, state:FSMContext):
    gender = callback.data
    await state.update_data({"worker_gender":gender})
    await state.set_state(WorkForm.workers)
    await callback.message.answer(_("Sizga nechta ishchi kerak?"),reply_markup=back_button())

@work_router.message(WorkForm.workers, F.text.isdigit())
async def save_work(message:Message, state:FSMContext):
    number = message.text
    employer_id = str(message.from_user.id)
    data = await state.get_data()
    await Work.create(title=data['title'],
                      category_id=data['category_id'],
                      price=data['price'],
                      description=data['description'],
                      photo_id=data['photo_id'],
                      latitude=data['latitude'],
                      longitude=data['longitude'],
                      worker_gender=data['worker_gender'],
                      num_of_workers=number,
                      employer_id=employer_id)


