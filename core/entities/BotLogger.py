import logging
from datetime import datetime
from typing import TextIO


class BotLogger:
    """
    Custom logger class for telegram bot / Locust test and С+ web doc.
    """

    __log_file: TextIO  # file for logs
    __logger: logging.Logger  # private instance of composite logger
    __is_file_write: bool  # is need write to file

    def __init__(self, name: str, is_file_write: bool = False):
        self.__logger = logging.getLogger(name)
        if is_file_write:
            self.__is_file_write = True
            self.__get_log_file()
        else:
            self.__is_file_write = False

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
            formated_msg = f"{(datetime.now())}: '{msg}'."
            if self.__is_file_write:
                self.__log_file.write(formated_msg)
                self.__logger.log(msg=formated_msg, stacklevel=stacklevel, level=level)
                print(formated_msg)
            else:
                self.__logger.log(msg=formated_msg, stacklevel=stacklevel, level=level)
                print(formated_msg)
        except Exception as e:
            print(f"Error occurred while writing log file - {e}")

    def __get_log_file(self):
        """
        Creates log file for bot actions
        :return: None
        """
        try:
            self.__log_file = open("../bot_logs_file.log")
        except Exception as e:
            print(f"{(datetime.now())}: Exception occurred in logger - {e}.")
            self.__log_file.close()

    def __close_log_file(self):
        """
        Closes log file
        :return: None
        """
        try:
            self.__log_file.close()
        except Exception as e:
            print(f"{(datetime.now())}: Error in closing log file - {e}.")

    def is_file_write(self):
        """
        Method for is writing info
        :return:
        """
        return self.__is_file_write

    def get_log_file(self):
        """
        Method for getting log file descriptor
        :return:
        """
        return self.__log_file

    def get_log_file_name(self):
        """
        Getter method for log file name
        """
        return self.__log_file.name

    def set_log_file_name(self):
        """
        Setter method for logger
        :return: None
        """
        pass
