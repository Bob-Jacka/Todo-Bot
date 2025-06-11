from aiogram.fsm.state import (
    StatesGroup,
    State
)


class AgeForm(StatesGroup):
    """
    User form
    """

    name = State()
    age = State()
    gender = State()
