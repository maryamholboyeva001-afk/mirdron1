from aiogram.fsm.state import State, StatesGroup


class Login(StatesGroup):
    scooter_id = State()
    model = State()
    device = State()


class Sos(StatesGroup):
    location = State()


class AlertFlow(StatesGroup):
    find_id = State()
    location = State()
    time = State()
    confirm = State()
