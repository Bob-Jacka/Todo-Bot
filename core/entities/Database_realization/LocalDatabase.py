from typing import Any

from typing_extensions import override

from core.entities.BotLogger import BotLogger
from core.entities.Database_realization.AbstractDatabase import AbstractDatabase
from core.entities.ToDoTask import ToDoTask


class LocalDatabase(AbstractDatabase):
    __database_name: str
    tables: dict[str, list[ToDoTask]]
    local_logger: BotLogger  # local logger for local database for local logging your local data.

    def __init__(self, base_name: str = 'local'):
        """
        Class for local key value database object.
        Class created only for testing. But if you want to use object, you can use it.
        :param base_name: name of the database
        """
        self.database_name = base_name
        self.tables = dict()
        self.local_logger = BotLogger("Localdb_" + base_name)
        self.local_logger.log(f"Local database created with name - '{base_name}'")

    ### Insert

    @override
    def insert_element(self, table_name: str, task: Any) -> bool:
        """
        Method for inserting one element
        :param table_name: name of the table
        :param task: task that need to insert into table
        :return: result of the operation
        """
        try:
            if not self.view_element(table_name, ""):
                self.tables[table_name].append(task)
                self.local_logger.log(f"Element - {task.get_name()} successfully inserted")
                return True
            else:
                self.local_logger.log('try to insert existing element')
                return False

        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")
            return False

    def insert_elements(self, table_name: str, *tasks: ToDoTask) -> bool:
        """
        Method for inserting a lot of elements
        :param table_name: name of the table
        :param tasks: tasks that need to insert into table
        :return: result of the operation
        """
        try:
            if not self.view_elements(table_name, ""):  # TODO передавать id из задач
                self.tables[table_name].append(*tasks)
                self.local_logger.log(f"Elements - {tasks} successfully inserted")
                return True
            else:
                self.local_logger.log("Try to insert element already existing elements")
                return False

        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")
            return False

    ### Create anything

    @override
    def create_table(self, table_name: str) -> bool:
        """
        Method for creating table
        :param table_name: name of the table
        :return: result of the operation
        """
        try:
            if not self.is_table_exists(table_name):
                self.tables[table_name] = list()
                self.local_logger.log(f"Table with name - {table_name} successfully created")
                return True
            else:
                self.local_logger.log("Try to update element already existing table")
                return False

        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")
            return False

    def create_tables(self, *table_name: tuple[str, ...]) -> bool:
        """
        Method for creating tables from given table names
        :param table_name: tuple of names of the tables
        :return: result of the operation
        """
        try:
            if not self.is_table_exists(*table_name):
                self.tables[*table_name] = list()
                self.local_logger.log(f"Tables with names - {table_name} successfully created")
                return True
            else:
                self.local_logger.log("Try to update element already existing tables")
                return False

        except Exception as e:
            self.local_logger.log(f"Exception during creating tables with names - {table_name} - {e}")
            return False

    @override
    def create_database(self) -> bool:
        pass

    ### Delete

    @override
    def delete_element(self, id: str) -> bool:
        """
        Method for deleting element from table.
        :param id: unique identifier
        :return: result of the operation
        """
        try:
            for list_task in self.tables.values():
                for task in list_task:
                    if task.get_name() == id:
                        pass
            return True
        except Exception as e:
            self.local_logger.log(f"Exception during delete element from table with id - {id} - {e}")
            return False

    @override
    def delete_table(self, id: str) -> bool:
        """
        Method for deleting table by given id
        :param id: unique identifier of the table
        :return: result of the operation
        """
        try:
            if self.is_table_exists(id):
                self.tables.pop(id)
                self.local_logger.log(f"Table with id - {id} successfully deleted")
                return True
            else:
                self.local_logger.log("Try to delete element no existing table")
                return False

        except Exception as e:
            self.local_logger.log(f"Exception during deleting element from table with id - {id} - {e}")
            return False

    def delete_tables(self, *ids: str) -> bool:
        """
        Method for deleting tables by given id's
        :param ids: unique identifiers of the tables
        :return: result of the operation
        """
        try:
            if self.is_table_exists(*ids):
                self.tables.pop(*ids)
                self.local_logger.log(f"Tables with id - {ids} successfully deleted")
                return True
            else:
                self.local_logger.log("Try to delete element no existing tables")
                return False

        except Exception as e:
            self.local_logger.log(f"Exception during deleting element - {e}")
            return False

    @override
    def delete_database(self) -> bool:
        pass

    ### Update

    @override
    def update_element(self, table_name: str, id: str) -> bool:
        """
        Method for updating table
        :param table_name: name of the table
        :param id: unique identifier
        :return: result of the operation
        """
        try:
            if self.view_element(table_name, id):
                self.tables[table_name][id] = None
                self.local_logger.log(f"Element with id - {id} from table - {table_name} successfully updated")
                return True
            else:
                self.local_logger.log("Try to update element no existing element")
                return False

        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")
            return False

    ### View

    @override
    def view_element(self, table_name: str, id: str) -> ToDoTask:
        """
        Method for viewing element in table by table name and id
        :param table_name: name of the table
        :param id: unique identifier
        :return: task entity
        """
        try:
            self.local_logger.log(f"Element with id - {id} from table - {table_name} successfully viewed")
            return self.tables.get(table_name)[id]

        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    @override
    def view_elements(self, table_name: str, *ids: str) -> tuple[ToDoTask]:
        """
        Method for selecting all from database
        :param table_name: name of the table
        :param ids: unique identifiers of elements
        :return: tasks entity
        """
        try:
            self.local_logger.log(f"Elements with ids - {ids} from table - {table_name} successfully viewed")
            return self.tables.get(table_name)[ids]

        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    ### Utility methods

    @override
    def is_table_exists(self, table_name: str) -> bool:
        """
        Utility function for checking if table exists
        :param table_name:
        :return: bool result of table existence
        """
        return False if self.tables.get(table_name) is not None else True

    @override
    def is_database_exists(self) -> bool:
        """
        Utility function for checking if database exists
        :return: bool result of database existence
        """
        return True if self.tables is not None and self.database_name else False
