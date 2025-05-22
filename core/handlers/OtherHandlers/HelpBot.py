from typing import Optional

from aiogram import MagicFilter
from aiogram.filters import Command

from core.handlers.ToDo_handlers.BotCommands import commands


class HelpBot(Command):
    """
    Handler command that will be interacted with "/help" command
    """

    ignore_case: bool
    ignore_mention: bool
    magic: Optional[MagicFilter]

    def __init__(self,
                 ignore_case: bool = False,
                 ignore_mention: bool = False,
                 magic: Optional[MagicFilter] = None):
        self.ignore_case = ignore_case,
        self.ignore_mention = ignore_mention,
        self.magic = magic,
        super().__init__(
            commands["helpBot"],
            prefix="/",
            ignore_case=ignore_case,
            ignore_mention=ignore_mention,
            magic=magic,
        )
