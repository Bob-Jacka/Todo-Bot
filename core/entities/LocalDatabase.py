from core.entities.BotLogger import BotLogger
from core.entities.ToDoTask import ToDoTask


class LocalDatabase:
    base_name: str
    tables: dict[str, list[ToDoTask]]
    local_logger: BotLogger  # local logger for local database for local logging your local data.

    def __init__(self, base_name: str = 'local'):
        """
        Class for local key value database object.
        Class created only for testing. But if you want to use object, you can use it.
        :param base_name: name of the database
        """
        self.base_name = base_name
        self.tables = dict()
        self.local_logger = BotLogger(base_name)

    ### Insert

    def insert_element(self, table_name: str, task: ToDoTask):
        """
        Method for inserting one element
        :param table_name: name of the table
        :param task:
        :return: none
        """
        try:
            self.tables[table_name].append(task)
            self.local_logger.log(f"Element - {task.get_name()} successfully inserted")
        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    def insert_elements(self, table_name: str, *task: ToDoTask):
        """
        Method for inserting a lot of elements
        :param table_name: name of the table
        :param task:
        :return: none
        """
        try:
            self.tables[table_name].append(*task)
            self.local_logger.log(f"Elements - {task} successfully inserted")
        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    ### Create

    def create_table(self, table_name: str):
        """
        Method for creating table
        :param table_name: name of the table
        :return: none
        """
        try:
            self.tables[table_name] = list()
            self.local_logger.log(f"Table with name - {table_name} successfully created")
        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    def create_tables(self, *table_name: str):
        """
        Method for creating tables from given table names
        :param table_name: tuple of names of the tables
        :return: none
        """
        try:
            self.tables[*table_name] = list()
            self.local_logger.log(f"Tables with names - {table_name} successfully created")
        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    ### Delete

    def delete_from_table(self, id: str):
        """
        Method for deleting element from table.
        :param id: unique identifier
        :return: none
        """
        try:
            for list_task in self.tables.values():
                for task in list_task:
                    if task.get_name() == id:
                        pass
        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    def delete_table(self, id: str):
        """
        Method for deleting table by given id
        :param id: unique identifier
        :return: none
        """
        try:
            self.tables.pop(id)
            self.local_logger.log(f"Table with id - {id} successfully deleted")
        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    def delete_tables(self, *id: str):
        """
        Method for deleting tables by given id's
        :param id: unique identifier
        :return: none
        """
        try:
            self.tables.pop(*id)
            self.local_logger.log(f"Tables with id - {id} successfully deleted")
        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    ### Update

    def update_table(self, table_name: str, id: str):
        """
        Method for updating table
        :param table_name: name of the table
        :param id: unique identifier
        :return: none
        """
        try:
            self.tables[table_name][id] = None
            self.local_logger.log(f"Element with id - {id} from table - {table_name} successfully updated")
        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    ### View

    def view_element(self, table_name: str, id: str) -> ToDoTask:
        """
        Method for viewing element
        :param table_name: name of the table
        :param id: unique identifier
        :return: none
        """
        try:
            self.local_logger.log(f"Element with id - {id} from table - {table_name} successfully viewed")
            return self.tables.get(table_name)[id]
        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")

    def view_elements(self, table_name: str, *id: str) -> tuple[ToDoTask]:
        """
        Method for selecting all from database
        :param table_name: name of the table
        :param id: unique identifier
        :return: none
        """
        try:
            self.local_logger.log(f"Elements with ids - {id} from table - {table_name} successfully viewed")
            return self.tables.get(table_name)[id]
        except Exception as e:
            self.local_logger.log(f"Exception during insert element - {e}")
