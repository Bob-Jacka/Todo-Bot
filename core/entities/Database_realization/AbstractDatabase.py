from abc import (
    ABC,
    abstractmethod
)
from typing import Any


class AbstractDatabase(ABC):
    """
    Abstract database class for other realizations, ex. mongo, postgres, local db, mysql

    If you need to implement Database, inherit this class and override methods
    """

    __database_name: str

    # elements methods in database

    @abstractmethod
    def insert_element(self, table_name: str, task: Any) -> bool:
        """
        Method for inserting element in table.
        Select * from <table name> is equivalent in sql for this statement
        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def view_element(self, table_name: str, id: str) -> None:
        """
        Method for viewing element from table.
        Select * from <table name> is equivalent in sql for this statement
        :return: None
        """
        pass

    @abstractmethod
    def update_element(self, table_name: str, id: str) -> bool:
        """
        Method for updating element in table.
        :param table_name: name of the table
        :param id: unique identifier of the element
        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def delete_element(self, id: str) -> bool:
        """
        Method for deleting element from table.
        :param id: unique identifier of the element
        :return: bool result of the operation
        """
        pass

    # table methods

    @abstractmethod
    def create_table(self, table_name: str) -> bool:
        """
        Method for creating table.
        :param table_name: name of the table to create
        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def delete_table(self, id: str) -> bool:
        """
        Method for deleting table.
        :param id: identifier of the table
        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def create_database(self) -> bool:
        """
        Method for creating database.
        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def delete_database(self) -> bool:
        """
        Method for deleting database.
        :return: bool result of the operation
        """
        pass

    # Utility methods

    @abstractmethod
    def is_table_exists(self, table_name: str) -> bool:
        """
        Helper function
        :param table_name:
        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def is_database_exists(self) -> bool:
        """
        Helper function
        :return: bool result of the operation
        """
        pass
