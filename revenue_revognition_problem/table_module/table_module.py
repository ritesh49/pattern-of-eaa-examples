from enum import Enum, unique


@unique
class ProductType(Enum):
    WP = 'WP'
    SS = 'SS'
    DB = 'DB'


class DataTable:
    pass


class DataSet:
    pass


class DataRow:
    pass


class TableModule:
    _table: DataTable

    def __init__(self, ds: DataSet, table_name: str):
        self._table = ds.tables[table_name]

