from typing import Any

from aiogram.filters import Filter
from aiogram.types import Message


class AdminFilter(Filter):

    def __init__(self, text: str, bot_config) -> None:
        self.text = text
        self.bot_config = bot_config

    async def __call__(self, message: Message) -> bool | dict[str, Any]:
        return message.from_user.id in self.bot_config.admin_ids
