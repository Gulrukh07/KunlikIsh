import asyncio
import os

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.media_group import MediaGroupBuilder

from bot.buttons.inline import employee_response, for_admin, deal_button
from bot.buttons.reply import back_button, rating
from bot.states import WorkForm
from db.models import Work, Employee, Employer, WorkStatus, Rating

admin_router = Router()
admin_id = os.getenv('ADMIN')


@admin_router.message(WorkForm.admin, F.text == __("Ha"))
async def admin_panel(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    employer_id = data.get('employer_id')
    chat_id = message.from_user.id
    await message.bot.send_message(chat_id=chat_id, text=_("Sizning buyurtmangiz adminga yuborildi\n"
                                                           "Iltimos, tasdiq javobini kuting 😊"))

    work = await Work.get_work_photos(employer_id)
    try:
        work_info = _(
            "🆔 Ish raqami: {id}\n"
            "📌 Ish nomi: {title}\n"
            "🗂️ Ish turi IDsi: {category}\n"
            "📝 Ish haqida: {description}\n"
            "💰 Ish narxi: {price}\n"
            "👥 Ishchilar soni: {num_of_workers}\n"
            "⚧️ Ishchining jinsi: {worker_gender}\n"
            "🧑‍💼 Ish beruvchi IDsi: {employer_id}\n"
            "📅 Buyurtma berilgan sana: {created_at}\n"
        ).format(
            id=work.id,
            title=work.title,
            category=work.category_id,
            description=work.description,
            price=work.price,
            num_of_workers=work.num_of_workers,
            worker_gender=work.worker_gender.value,
            employer_id=work.employer_id,
            created_at=work.created_at.strftime("%Y-%m-%d")
        )
        if work.photos:
            if len(work.photos) == 1:
                await message.bot.send_photo(
                    chat_id=admin_id,
                    photo=work.photos[0].photo_id
                )
            else:
                builder = MediaGroupBuilder()
                for photo in work.photos:
                    builder.add_photo(media=photo.photo_id)
                await message.bot.send_media_group(chat_id=admin_id, media=builder.build())
        lat = work.latitude
        long = work.longitude
        await bot.send_location(chat_id=admin_id, latitude=lat, longitude=long)
        await state.update_data(admin=message.from_user.id)
        await state.update_data(employer_id=chat_id)
        await bot.send_message(
            chat_id=admin_id,
            text=f"🆕 Yangi buyurtma :\n\n{work_info}\n\nQabul qilamizmi?",
            reply_markup=for_admin()
        )

    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")


@admin_router.callback_query(F.data.startswith("successfully"))
async def handler_admin_response(callback: CallbackQuery):
    employer_id = int(callback.message.text.split(":")[9][1])
    employer = await Employer.get(_id=employer_id)
    await callback.bot.send_message(chat_id=employer.chat_id, text=_("🎉 Tabriklaymiz, sizning buyurtmangiz "
                                                                     "admin tomonidan qabul qilindi\n"
                                                                     "U ishchilar tomonidan qabul qilinsa, "
                                                                     "biz sizga xabar beramiz"),
                                    reply_markup=back_button())
    work = await Work.get_work_photos(employer_id=employer.id)
    work_id = work.id
    work_info = _(
        "📌 Ish nomi: {title}\n"
        "📝 Ish haqida: {description}\n"
        "💰 Ish narxi: {price}\n"
        "👥 Ishchilar soni: {num_of_workers}\n"
        "⚧️ Ishchining jinsi: {worker_gender}\n"
        "📅 Buyurtma berilgan sana: {created_at}\n"
    ).format(
        title=work.title,
        description=work.description,
        price=work.price,
        num_of_workers=work.num_of_workers,
        worker_gender=work.worker_gender.value,
        created_at=work.created_at.strftime("%Y-%m-%d")
    )
    employees = await Employee.get_all()
    employee_ids = [employee.chat_id for employee in employees]
    for employee_id in employee_ids:
        await callback.bot.send_message(chat_id=employee_id,
                                        text=_("Yangi Buyurtma:\n\n{work_info}").format(work_info=work_info)
                                             + _("\n\nQabul qilasizmi?"),
                                        reply_markup=employee_response(employer.chat_id, work_id))

        if work.photos:
            if len(work.photos) == 1:
                await callback.bot.send_photo(
                    chat_id=employee_id,
                    photo=work.photos[0].photo_id
                )
            else:
                builder = MediaGroupBuilder()
                for photo in work.photos:
                    builder.add_photo(media=photo.photo_id)
                await callback.bot.send_media_group(chat_id=employee_id, media=builder.build())
        lat = work.latitude
        long = work.longitude
        await callback.bot.send_location(chat_id=employee_id, latitude=lat, longitude=long)


@admin_router.callback_query(F.data.startswith("rejected"))
async def admin_response1(callback: CallbackQuery):
    employer_id = int(callback.message.text.split(":")[9][1])
    employer = await Employer.get(_id=employer_id)
    await callback.bot.send_message(chat_id=employer.chat_id, text=_("☹️ Afsuski, Sizning buyurtmangiz rad etildi"),
                                    reply_markup=back_button())


@admin_router.callback_query(F.data.startswith("accepted"))
async def admin_response1(callback: CallbackQuery, bot: Bot, state: FSMContext):
    employer_id = int(callback.data.split("_")[-2])
    work_id = int(callback.data.split("_")[-1])
    employee_id = callback.from_user.id
    employee = await Employee.get(telegram_id_=employee_id)
    ee_id = employee.id
    employer = await Employer.get(telegram_id_=employer_id)
    er_id = employer.id
    phone = employee.phone_number
    employee_username = callback.from_user.username if callback.from_user.username else None

    if employee_username:
        await bot.send_message(chat_id=employer_id,
                               text=_("📌 Buyurtmangiz @{employee_username} tomondan qabul qilindi\n"
                                      "Ishchi bilan kelishgandan so'ng xabar bering⁉").format(
                                   employee_username=employee_username),
                               reply_markup=deal_button(employee_id=ee_id, employer_id=er_id))
    else:
        await bot.send_message(chat_id=employer_id, text=_("📌 Buyurtmangiz {phone} qabul qilindi\n"
                                                           f"Ishchi bilan kelishgandan so'ng xabar bering⁉").format(
            phone=phone), reply_markup=deal_button(employee_id=ee_id, employer_id=er_id))

    await bot.send_message(
        chat_id=admin_id,
        text=_(
            "📢 {employer_id} - sonli ish beruvchining {work_id} - sonli buyurtmasi {employee_id} - sonli ishchi tomonidan qabul qilindi").format(
            employer_id=employer.id,
            work_id=work_id,
            employee_id=employee.id
        )
    )


@admin_router.callback_query(F.data.startswith("deal"))
async def deal_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    employer_id = int(callback.data.split("/")[-1])
    employee_id = int(callback.data.split("/")[-2])
    await state.set_state(WorkForm.rating)
    employer = await Employer.get(_id=employer_id)
    employer_chat_id = employer.chat_id
    employee = await Employee.get(_id=employee_id)
    employee_username = employee.username if employee.username else employee.phone_number
    work = await Work.filter(employer_id=employer_id)
    work_id = work[-1].id
    await state.update_data(work_id=work_id)
    await Work.update(_id=work_id, status=WorkStatus.Done)
    await Work.update(_id=work_id, employee_id=employee_id)

    await bot.send_message(chat_id=admin_id, text=_("{employer_id} - sonli buyurtmachining"
                                                    " {work_id} - sonli buyurtmasi {employee_id} - sonli ishchi bilan kelishildi ")
                           .format(employer_id=employer_id,
                                   work_id=work_id,
                                   employee_id=employee_id)
                           )
    await asyncio.sleep(5)
    await bot.send_message(chat_id=employer_chat_id,
                           text=_(f"Ish Tugallangandan so'ng @{employee_username} ishchini ishini baxolang?"),
                           reply_markup=rating())


@admin_router.message(WorkForm.rating, F.text.in_(["5", "4", "3", "2", "1"]))
async def rating_handler(message: Message, state: FSMContext):
    rating = int(message.text)
    await state.update_data(rating=rating)
    await message.answer(_("Iltimos, bu baxoyingiz uchun izoh qoldiring"), reply_markup=ReplyKeyboardRemove())


@admin_router.message(WorkForm.rating, F.text)
async def feedback(message: Message, state: FSMContext):
    data = await state.get_data()
    feedback = message.text

    await Rating.create(
        rating=data["rating"],
        feedback=feedback,
        work_id=data["work_id"]
    )
    await message.answer(_("Botimizdan foydalanganingiz uchun raxmat 🙂"), reply_markup=back_button())
