from core.entities.BotLogger import BotLogger
from core.entities.Database_realization.AbstractDatabase import AbstractDatabase
from core.entities.Database_realization.LocalDatabase import LocalDatabase
from core.entities.Database_realization.Nosql.CassandraDatabase import CassandraDatabase
from core.entities.Database_realization.Nosql.MongoDatabase import MongoDatabase
from core.entities.Database_realization.Nosql.Neo4jDatabase import Neo4jDatabase
from core.entities.Database_realization.Nosql.RedisDatabase import RedisDatabase
from core.entities.Database_realization.Sql.MySqlDatabase import MySqlDatabase
from core.entities.Database_realization.Sql.PostgresDatabase import PostgresDatabase
from core.entities.Database_realization.Sql.SqliteDatabase import SqliteDatabase
from core.entities.Database_realization.ValidDatabasesType import ValidDatabasesType
from core.entities.ToDoTask import ToDoTask


class DatabaseController:
    """
    Database controller entity.
    Responsible for creating, updating, deleting and viewing data from database.
    Database indifferent controller entity
    """

    __base_name: str
    __base_type: ValidDatabasesType  # type maybe sqlite, postgres or mysql
    __is_static: bool  # if true - creates local key-value database
    __logger: BotLogger  # local logger entity

    database: AbstractDatabase  # single entity of database in controller

    def __init__(self, base_name: str, base_type: ValidDatabasesType, is_static_base: bool = False):
        """
        Base controller
        :param base_name: name of database
        :param base_type: type of the database in enum
        :param is_static_base: special param for local bases
        """
        self.__base_name = base_name
        self.__base_type = base_type
        self.__is_static = is_static_base
        self.__logger = BotLogger("Database_logger_" + base_name)

    def create_database(self, database_name: str):
        """
        Method for creating database entity with given name.
        :param database_name: name of the database
        :return: none
        """
        if self.__is_static:
            self.database: LocalDatabase = LocalDatabase()
            self.__logger.log('Local database created')
        else:
            abstract: AbstractDatabase
            match self.__base_type:

                case ValidDatabasesType.MONGO:
                    abstract = MongoDatabase()
                    self.__logger.log("Mongo db created")

                case ValidDatabasesType.CASSANDRA:
                    abstract = CassandraDatabase()
                    self.__logger.log("Cassandra db created")

                case ValidDatabasesType.NEO4J:
                    abstract = Neo4jDatabase()
                    self.__logger.log("Neo4j db created")

                case ValidDatabasesType.REDIS:
                    abstract = RedisDatabase()
                    self.__logger.log("Redis db created")

                case ValidDatabasesType.MY_SQL:
                    abstract = MySqlDatabase()
                    self.__logger.log("MySql db created")

                case ValidDatabasesType.SQLITE:
                    abstract = SqliteDatabase()
                    self.__logger.log("sqlite db created")

                case ValidDatabasesType.POSTGRES:
                    abstract = PostgresDatabase()
                    self.__logger.log("Postgres db created")

                case _:
                    self.__logger.log(f"database does not support - {self.__base_type}")

            self.database = abstract
            self.__logger.log(f"Database created with name - '{database_name}'")

    def create_table(self, table_name: str) -> bool:
        """
        Method for creating database table
        :param table_name: name of the table
        :return: result of the operation
        """
        if self.__is_static:
            self.database.create_table(table_name)
            self.__logger.log(f"Create table with name - '{table_name}'")
            return True
        else:
            self.__logger.log(f"Create table with name - '{table_name}'")
            return True

    ##############Delete

    def delete_table(self, table_name: str) -> bool:
        """
        Method for deleting database table
        :param table_name: name of the table
        :return: result of the operation
        """
        if self.__is_static:
            if self.is_table_created(table_name):
                self.database.delete_table(table_name)
                self.__logger.log(f"Delete entity in table - '{table_name}'")
                return True
            else:
                return False
        else:
            self.__logger.log(f"Delete entity in table - '{table_name}'")
            return False

    def delete_element_from_table(self, table_name: str, id: str):
        """
        Method for deleting database table
        :param table_name: name of the table
        :param id: unique identifier of the element in database
        :return: none
        """
        if self.__is_static:
            self.database.delete_element(id)
            self.__logger.log(f"Delete entity with id - {id} in table - '{table_name}'")
        else:
            self.__logger.log(f"Delete entity with id - {id} in table - '{table_name}'")

    def delete_database(self, database_name: str) -> bool:
        """
        Method for deleting database entity
        :param database_name: name of the database
        :return: result of the operation
        """
        if self.__is_static:
            self.__logger.log(f"Delete database in local db is not allowed")
            return False
        else:
            if self.database.is_database_exists():
                self.database.delete_database()
                self.__logger.log(f"Delete database with name - '{database_name}'")
                return True
            else:
                self.__logger.log("Try to delete no exist database")
                return False

    ##############Select from database

    def select_one_from_table(self, table_name: str, id: str) -> ToDoTask | None:
        """
        Method for selecting one element from database table
        :param table_name: name of the table
        :param id: unique identifier of the element in database
        :return: none or task entity from table
        """
        if self.__is_static:
            self.__logger.log(f"Select one entity with id - '{id}' in table - '{table_name}'")
            return self.database.view_element(table_name, id)
        else:
            self.__logger.log(f"Select one entity with id - '{id}' in table - '{table_name}'")

    def select_all_from_table(self, table_name: str):
        """
        Method for selecting all entities from database table
        :param table_name: name of the table
        :return: tuple value with all elements
        """
        if self.__is_static:
            all_elements = self.database.view_elements(table_name)
            self.__logger.log(f"Access all entities in table - '{table_name}'")
            return all_elements
        else:
            self.__logger.log(f"Access all entities in table - '{table_name}'")

    def select_all_from_database(self, database: str):
        """
        Method for selecting all entities from database
        :param database: name of the database
        :return: none
        """
        if self.__is_static:
            self.__logger.log("Operation does not allowed in local database")
        else:
            self.__logger.log(f"Access all entities in database - '{database}'")

    ##############Update and insert

    def update_entity_in_table(self, table_name: str, id: str):
        """
        Method for updating database table
        :param id: unique identifier of the element in database
        :param table_name: name of the table
        :return: none
        """
        if self.__is_static:
            self.database.update_element(table_name, id)
            self.__logger.log(f"Update entity with id - {id} in table - '{table_name}'")
        else:
            self.__logger.log(f"Update entity with id - {id} in table - '{table_name}'")

    def insert_entity_in_table(self, table_name: str, id: str, elem: ToDoTask):
        """
        Method for updating database table
        :param elem: element to insert
        :param id: unique identifier of the element in database
        :param table_name: name of the table
        :return: none
        """
        if self.__is_static:
            if self.database.is_table_exists(table_name):
                self.database.insert_element(table_name, elem)
                self.__logger.log(f"Entity with id - {id} inserted in table - '{table_name}'")
        else:
            self.__logger.log(f"Entity with id - {id} inserted in table - '{table_name}'")

    def insert_user_in_table(self, table_name: str, id: int, user):
        """
        Method for updating database table
        Semantically equal to insert_entity_in_table, but need user as function input
        And different logs output
        :param user: user to insert in table
        :param id: unique identifier of the user in database, int value from message
        :param table_name: name of the table
        :return: none
        """
        if self.__is_static:
            if self.database.is_table_exists(table_name):
                self.database.insert_element(table_name, user)
                self.__logger.log(f"User with id - {id} inserted in table - '{table_name}'")
        else:
            self.__logger.log(f"User with id - {id} inserted in table - '{table_name}'")

    ##############Utility methods

    def is_database_created(self) -> bool:
        """
        Helper function
        """
        return self.database.is_database_exists()

    def is_table_created(self, table_name) -> bool:
        """
        Helper function
        """
        return self.database.is_table_exists(table_name)

    def is_user_exists(self, table_name: str, id: str):
        """
        Helper function
        """
        return self.database.view_element(table_name, id)

    def get_database_name(self):
        """
        Helper function
        """
        return self.database.database_name
