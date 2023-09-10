from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    check_old_password = State()
    get_new_password = State()
