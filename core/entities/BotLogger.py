from datetime import datetime
from logging import Logger
from typing import TextIO

from typing_extensions import override


class BotLogger(Logger):
    """
    Custom logger class for telegram bot.
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

    @override
    def log(self, msg: str, *args, level=1, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        """
        Method for writing logs
        :param msg: message to be written
        :param args:
        :param level: level of logging, 1 by default
        :param exc_info:
        :param stack_info:
        :param stacklevel:
        :param extra:
        :return: None
        """
        try:
            formated_msg = f"{(datetime.now())}: {msg}."
            if self.is_file_write:
                self.log_file.write(formated_msg)
                print(formated_msg)
            else:
                print(formated_msg)
        except Exception as e:
            print(f"Error occurred while writing log file - {e}")

    def __get_log_file(self):
        """
        Creates log file for bot actions
        :return: None
        """
        try:
            self.log_file = open("../bot_logs_file.log")
        except Exception as e:
            print(f"{(datetime.now())}: Exception occurred in logger - {e}.")
            self.log_file.close()

    def __close_log_file(self):
        """
        Closes log file
        :return: None
        """
        try:
            self.log_file.close()
        except Exception as e:
            print(f"{(datetime.now())}: Error in closing log file - {e}.")

    def is_file_write(self):
        """
        Method for is writing info
        :return:
        """
        return self.is_file_write

    def get_log_file(self):
        """
        Method for getting log file descriptor
        :return:
        """
        return self.log_file

    @override
    def setLevel(self, level):
        super().setLevel(level)

    @override
    def debug(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        super().debug(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    @override
    def info(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        super().info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    @override
    def warning(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        super().warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    @override
    def warn(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        super().warn(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    @override
    def error(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        super().error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    @override
    def exception(self, msg, *args, exc_info=True, stack_info=False, stacklevel=1, extra=None):
        super().exception(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)

    @override
    def critical(self, msg, *args, exc_info=None, stack_info=False, stacklevel=1, extra=None):
        super().critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
