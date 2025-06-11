from core.entities.Database_realization.AbstractDatabase import AbstractDatabase


class SqliteDatabase(AbstractDatabase):
    def insert_element(self) -> bool:
        pass

    def view_element(self) -> None:
        pass

    def update_element(self) -> bool:
        pass

    def delete_element(self, id: str) -> bool:
        pass

    def create_table(self, table_name: str) -> bool:
        pass

    def delete_table(self, id: str) -> bool:
        pass

    def create_database(self) -> bool:
        pass

    def delete_database(self) -> bool:
        pass

    def is_table_exists(self, table_name: str) -> bool:
        pass

    def is_database_exists(self) -> bool:
        pass
