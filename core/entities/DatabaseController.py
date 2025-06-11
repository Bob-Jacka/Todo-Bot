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

    base_name: str
    base_type: ValidDatabasesType  # type maybe sqlite, postgres or mysql
    is_static: bool  # if true - creates local key-value database
    logger: BotLogger  # local logger entity

    database: AbstractDatabase  # single entity of database in controller

    def __init__(self, base_name: str, base_type: ValidDatabasesType, is_static_base: bool = False):
        """
        Base controller
        :param base_name: name of database
        :param base_type: type of the database in enum
        :param is_static_base: special param for local bases
        """
        self.base_name = base_name
        self.base_type = base_type
        self.is_static = is_static_base
        self.logger = BotLogger("Database_logger_" + base_name)

    def create_database(self, database_name: str):
        """
        Method for creating database entity with given name.
        :param database_name: name of the database
        :return: none
        """
        if self.is_static:
            self.database: LocalDatabase = LocalDatabase()
        else:
            abstract: AbstractDatabase
            match self.base_type:

                case ValidDatabasesType.MONGO:
                    abstract = MongoDatabase()
                    self.logger.log("Mongo db created")

                case ValidDatabasesType.CASSANDRA:
                    abstract = CassandraDatabase()
                    self.logger.log("Cassandra db created")

                case ValidDatabasesType.NEO4J:
                    abstract = Neo4jDatabase()
                    self.logger.log("Neo4j db created")

                case ValidDatabasesType.REDIS:
                    abstract = RedisDatabase()
                    self.logger.log("Redis db created")

                case ValidDatabasesType.MY_SQL:
                    abstract = MySqlDatabase()
                    self.logger.log("MySql db created")

                case ValidDatabasesType.SQLITE:
                    abstract = SqliteDatabase()
                    self.logger.log("sqlite db created")

                case ValidDatabasesType.POSTGRES:
                    abstract = PostgresDatabase()
                    self.logger.log("Postgres db created")

                case _:
                    self.logger.log(f"database does not support - {self.base_type}")

            self.database = abstract
            self.logger.log(f"Database created with name - '{database_name}'")

    def create_table(self, table_name: str) -> bool:
        """
        Method for creating database table
        :param table_name: name of the table
        :return: result of the operation
        """
        if self.is_static:
            self.database.create_table(table_name)
            self.logger.log(f"Create table with name - '{table_name}'")
            return True
        else:
            self.logger.log(f"Create table with name - '{table_name}'")
            return True

    ##############Delete

    def delete_table(self, table_name: str) -> bool:
        """
        Method for deleting database table
        :param table_name: name of the table
        :return: result of the operation
        """
        if self.is_static:
            if self.is_table_created(table_name):
                self.database.delete_table(table_name)
                self.logger.log(f"Delete entity in table - '{table_name}'")
                return True
            else:
                return False
        else:
            self.logger.log(f"Delete entity in table - '{table_name}'")
            return False

    def delete_element_from_table(self, table_name: str, id: str):
        """
        Method for deleting database table
        :param table_name: name of the table
        :param id: unique identifier of the element in database
        :return: none
        """
        if self.is_static:
            self.database.delete_element(id)
            self.logger.log(f"Delete entity with id - {id} in table - '{table_name}'")
        else:
            self.logger.log(f"Delete entity with id - {id} in table - '{table_name}'")

    def delete_database(self, database_name: str) -> bool:
        """
        Method for deleting database entity
        :param database_name: name of the database
        :return: result of the operation
        """
        if self.is_static:
            self.logger.log(f"Delete database in local db is not allowed")
            return False
        else:
            if self.database.is_database_exists():
                self.database.delete_database()
                self.logger.log(f"Delete database with name - '{database_name}'")
                return True
            else:
                self.logger.log("Try to delete no exist database")
                return False

    ##############Select from database

    def select_one_from_table(self, table_name: str, id: str) -> ToDoTask | None:
        """
        Method for selecting one element from database table
        :param table_name: name of the table
        :param id: unique identifier of the element in database
        :return: none or task entity from table
        """
        if self.is_static:
            self.logger.log(f"Select one entity with id - '{id}' in table - '{table_name}'")
            return self.database.view_element(table_name, id)
        else:
            self.logger.log(f"Select one entity with id - '{id}' in table - '{table_name}'")

    def select_all_from_table(self, table_name: str):
        """
        Method for selecting all entities from database table
        :param table_name: name of the table
        :return: tuple value with all elements
        """
        if self.is_static:
            all_elements = self.database.view_elements(table_name)
            self.logger.log(f"Access all entities in table - '{table_name}'")
            return all_elements
        else:
            self.logger.log(f"Access all entities in table - '{table_name}'")

    def select_all_from_database(self, database: str):
        """
        Method for selecting all entities from database
        :param database: name of the database
        :return: none
        """
        if self.is_static:
            self.logger.log("Operation does not allowed in local database")
        else:
            self.logger.log(f"Access all entities in database - '{database}'")

    ##############Update and insert

    def update_entity_in_table(self, table_name: str, id: str):
        """
        Method for updating database table
        :param id: unique identifier of the element in database
        :param table_name: name of the table
        :return: none
        """
        if self.is_static:
            self.database.update_element(table_name, id)
            self.logger.log(f"Update entity with id - {id} in table - '{table_name}'")
        else:
            self.logger.log(f"Update entity with id - {id} in table - '{table_name}'")

    def insert_entity_in_table(self, table_name: str, id: str, elem: ToDoTask):
        """
        Method for updating database table
        :param elem: element to insert
        :param id: unique identifier of the element in database
        :param table_name: name of the table
        :return: none
        """
        if self.is_static:
            if self.database.is_table_exists(table_name):
                self.database.insert_element(table_name, elem)
                self.logger.log(f"Entity with id - {id} inserted in table - '{table_name}'")
        else:
            self.logger.log(f"Entity with id - {id} inserted in table - '{table_name}'")

    ##############Utility methods

    def is_database_created(self) -> bool:
        return self.database.is_database_exists()

    def is_table_created(self, table_name) -> bool:
        return self.database.is_table_exists(table_name)

    def get_database_name(self):
        return self.database.database_name
