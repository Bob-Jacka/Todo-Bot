from typing import Any

from aiogram.filters import Filter
from aiogram.types import Message


class TextFilter(Filter):

    def __init__(self, text: str) -> None:
        self.text = text

    async def __call__(self, message: Message) -> bool | dict[str, Any]:
        return message.text == self.text
