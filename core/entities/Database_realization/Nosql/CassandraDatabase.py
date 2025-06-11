from core.entities.Database_realization.AbstractDatabase import AbstractDatabase


class CassandraDatabase(AbstractDatabase):
    def insert_element(self) -> bool:
        pass

    def view_element(self, table_name: str, id: str) -> None:
        pass

    def update_element(self, table_name: str, id: str) -> bool:
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