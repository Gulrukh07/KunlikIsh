from aiogram.fsm.state import StatesGroup, State


class EmployerForm(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    main_panel = State()
    settings = State()
    about_me = State()
    update_name = State()
    update_lname = State()
    update_contact = State()


class EmployeeForm(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    gender = State()
    work_type = State()
    work_description = State()
    main_panel = State()
    settings = State()
    about_me = State()
    update_name = State()
    update_lname = State()
    update_contact = State()
    update_gender = State()
    update_work_t = State()
    update_work_d = State()
    my_ratings = State()


class WorkForm(StatesGroup):
    title = State()
    category = State()
    description = State()
    price = State()
    gender = State()
    photo = State()
    location = State()
    workers = State()
    admin = State()
    rating = State()


class BotState(StatesGroup):
    lang = State()
