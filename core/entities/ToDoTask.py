from aiogram.fsm.state import State, StatesGroup


class ToDoTask(StatesGroup):
    """
    Class representing to_do task entity, with parameters
    """

    Name = State()  # Task name
    Description = State()
    Sub_steps = State()
    is_expirable = State()
    Due_date = State()

    def __init__(self):
        super().__init__()

    def get_name(self):
        return self.Name

    def get_description(self):
        return self.Description

    def get_sub_steps(self):
        return self.Sub_steps

    def get_is_expire(self):
        return self.is_expirable

    def get_due_date(self):
        return self.Due_date
