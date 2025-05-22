from core.entities.ToDoTask import ToDoTask


class LocalDatabase:
    base_name: str
    tables: dict[str, list[ToDoTask]]

    def __init__(self, base_name: str = 'local'):
        self.base_name = base_name

    def create_table(self, table_name: str):
        self.tables[table_name] = list()

    def delete_table(self, id: str):
        self.tables.pop(id)

    def update_table(self, table_name: str, id: str):
        self.tables.update[table_name][id] = None

    def view_element(self, table_name: str, id: str) -> ToDoTask:
        return self.tables.get(table_name)[id]
