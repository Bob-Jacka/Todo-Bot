from abc import (
    ABC,
    abstractmethod
)


class AbstractDatabase(ABC):
    """
    Abstract database class for other realizations, ex. mongo, postgres, local db, mysql

    If you need to implement Database, inherit this class and override methods
    """

    database_name: str

    # elements methods in database

    @abstractmethod
    def insert_element(self) -> bool:
        """
        Method for viewing element from table.
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

        :param table_name: name of the table
        :param id: unique identifier of the element
        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def delete_element(self, id: str) -> bool:
        """

        :param id: unique identifier of the element
        :return: bool result of the operation
        """
        pass

    # table methods

    @abstractmethod
    def create_table(self, table_name: str) -> bool:
        """

        :param table_name: name of the table to create
        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def delete_table(self, id: str) -> bool:
        """

        :param id: identifier of the table
        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def create_database(self) -> bool:
        """

        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def delete_database(self) -> bool:
        """

        :return: bool result of the operation
        """
        pass

    # Utility methods

    @abstractmethod
    def is_table_exists(self, table_name: str) -> bool:
        """

        :param table_name:
        :return: bool result of the operation
        """
        pass

    @abstractmethod
    def is_database_exists(self) -> bool:
        """

        :return: bool result of the operation
        """
        pass
