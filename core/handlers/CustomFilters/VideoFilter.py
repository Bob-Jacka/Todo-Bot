from io import BytesIO

from aiogram import Bot
from aiogram.filters import Filter
from aiogram.types import Message


class VideoFilter(Filter):

    def __init__(self, text: str, bot_entity: Bot) -> None:
        self.text = text
        self.bot = bot_entity

    async def __call__(self, message: Message) -> dict[str, BytesIO] | None:
        if message.photo:
            file_id = message.photo.file_id
            file = await self.bot.get_file(file_id)
            file_data: BytesIO = await self.bot.download_file(file.file_path)
            return {"video_file": file_data}
