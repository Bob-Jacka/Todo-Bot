from typing import Literal

from core.entities.BotLogger import BotLogger
from core.entities.LocalDatabase import LocalDatabase
from core.entities.ToDoTask import ToDoTask


class DatabaseController:
    """
    Database controller entity.
    Responsible for creating, updating, deleting and viewing data from database.
    """

    base_name: str
    base_type: Literal['sqlite', 'mysql', 'postgres', 'local']  # type maybe sqlite, postgres or mysql
    is_static: bool
    logger: BotLogger
    static_data_base: LocalDatabase  # Super local database entity
    database_name: str = None

    def __init__(self, base_name: str, base_type: Literal['sqlite', 'mysql', 'postgres', 'local'], is_static_base: bool = False):
        """
        Base controller
        :param base_name: name of database
        """
        self.base_name = base_name
        self.base_type = base_type
        self.is_static = is_static_base
        self.logger = BotLogger("Database self.logger")

    def create_database(self, database_name: str):
        """
        Method for creating database entity
        :param database_name: name of the database
        :return: none
        """
        if self.is_static:
            self.static_data_base: LocalDatabase = LocalDatabase()
            self.logger.log(f"Local database created with name - {database_name}")
        else:
            # TODO в зависимости от базы данных необходимо проверить - есть ли база данных
            self.database_name = database_name
            self.logger.log(f"Database created with name - {database_name}")

    def create_table(self, table_name: str):
        """
        Method for creating database table
        :param table_name: name of the table
        :return: none
        """
        if self.is_static:
            self.static_data_base.create_table(table_name)
            self.logger.log(f"Create table with name - {table_name}.")
        else:
            self.logger.log(f"Create table with name - {table_name}.")

    ##############Delete

    def delete_table(self, table_name: str):
        """
        Method for deleting database table
        :param table_name: name of the table
        :return: none
        """
        if self.is_static:
            self.static_data_base.delete_table(table_name)
            self.logger.log(f"Delete entity in table - {table_name}.")
        else:
            self.logger.log(f"Delete entity in table - {table_name}.")

    def delete_element_from_table(self, table_name: str, id: str):
        """
        Method for deleting database table
        :param table_name: name of the table
        :param id: unique identifier of the element in database
        :return: none
        """
        if self.is_static:
            self.logger.log(f"Delete entity with id - {id} in table - {table_name}.")
        else:
            self.logger.log(f"Delete entity with id - {id} in table - {table_name}.")

    ##############Select

    def select_one_from_table(self, table_name: str, id: str) -> ToDoTask | None:
        """
        Method for selecting one element from database table
        :param table_name: name of the table
        :param id: unique identifier of the element in database
        :return: none
        """
        if self.is_static:
            self.logger.log(f"Select one entity with id - {id} in table - {table_name}.")
            return self.static_data_base.view_element(table_name, id)
        else:
            self.logger.log(f"Select one entity with id - {id} in table - {table_name}.")

    def select_all_from_table(self, table_name: str):
        """
        Method for selecting all entities from database table
        :param table_name: name of the table
        :return: none
        """
        if self.is_static:
            self.logger.log("Operation does not allowed in local database.")
        else:
            self.logger.log(f"Access all entities in table - {table_name}.")

    ##############Update and insert

    def update_entity_in_table(self, table_name: str, id: str):
        """
        Method for updating database table
        :param id: unique identifier of the element in database
        :param table_name: name of the table
        :return: none
        """
        if self.is_static:
            self.static_data_base.update_table(table_name, id)
            self.logger.log(f"Update entity with id - {id} in table - {table_name}.")
        else:
            self.logger.log(f"Update entity with id - {id} in table - {table_name}.")

    def insert_entity_in_table(self, table_name: str, id: str, elem: ToDoTask):
        """
        Method for updating database table
        :param elem:
        :param id: unique identifier of the element in database
        :param table_name: name of the table
        :return: none
        """
        if self.is_static:
            self.logger.log(f"Entity with id - {id} inserted in table - {table_name}.")
        else:
            self.logger.log(f"Entity with id - {id} inserted in table - {table_name}.")

    ##############Utility methods

    def is_database_created(self) -> bool:
        return self.database_name is not None

    def is_table_created(self, table_name) -> bool:
        pass

    def get_base_name(self):
        return self.database_name
