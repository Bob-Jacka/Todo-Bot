from logging import Logger
from typing import TextIO


class BotLogger(Logger):
    """
    Custom logger class for telegram bot
    """

    log_file: TextIO
    is_file_write: bool

    def __init__(self, name: str, is_file_write: bool = False):
        super().__init__(name)
        if is_file_write:
            self.is_file_write = True
            self.__get_log_file()
        else:
            self.is_file_write = False

    def log(
            self,
            msg: str,
            *args,
            level=1,
            exc_info=None,
            stack_info=False,
            stacklevel=1,
            extra=None,
    ):
        try:
            if self.is_file_write:
                self.log_file.write(msg)
                print(msg)
            else:
                print(msg)
        except Exception as e:
            print(f"Error occurred while writing log file - {e}")

    def __get_log_file(self):
        """
        Creates log file for bot actions
        :return:
        """
        try:
            self.log_file = open("../logs_file.log")
        except Exception as e:
            print(f"Exception occurred in logger - {e}")
            self.log_file.close()
