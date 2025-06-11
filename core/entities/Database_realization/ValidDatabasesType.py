from enum import Enum


class ValidDatabasesType(Enum):
    # no sql
    MONGO = 'mongo'
    CASSANDRA = 'cassandra'
    NEO4J = 'neo4j'
    REDIS = 'redis'

    # sql
    MY_SQL = 'mysql'
    POSTGRES = 'postgres'
    SQLITE = 'sqlite'

    # special
    LOCAL = 'local'
