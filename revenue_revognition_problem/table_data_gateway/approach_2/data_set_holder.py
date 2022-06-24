from ..mongodb import DatabaseClient, MongoDB, MONGO_DATABASE, CollectionClient
from bson.objectid import ObjectId


class DataSet:
    pass


class DataRow:
    pass


class DataTable:
    pass


class DataSetHolder:
    data: DataSet = DataSet()
    data_adapters: dict = {}

    def fill_data(self, table_name: str):
        da = DatabaseClient()[MONGO_DATABASE][table_name]
        da.insert(self.data)
        self.data_adapters.update({table_name: da})

    def update(self):
        for table in self.data_adapters:
            self.data_adapters[table].update(self.data)

    def __getitem__(self, table_name: str) -> DataTable:
        return self.data.tables[table_name]


class DataGateway:
    holder: DataSetHolder

    def __init__(self, collection_name: str):
        self.__collection_name = collection_name

    @property
    def data(self):
        pass

    @data.getter
    def data(self):
        return self.holder.data

    def load_all(self):
        self.holder.fill_data({}, self.__collection_name)

    def load_with_filter(self, filters: dict):
        self.holder.fill_data(filters, self.__collection_name)

    @property
    def collection(self) -> MongoDB:
        return DatabaseClient()[MONGO_DATABASE][self.__collection_name]

    def insert(self, last_name: str, first_name: str, number_of_dependents: int):
        key = ObjectId()
        new_row = self.table.new_row()
        new_row.update({
            '_id': key,
            'last_name': last_name,
            'first_name': first_name,
            'number_of_dependents': number_of_dependents
        })
        self.table.add(new_row)
        return key

    def update(self, key: str, last_name: str, first_name: str, number_of_dependents: int):
        ds: DataRow = self[key]
        ds['first_name'] = first_name
        ds['last_name'] = last_name
        ds['number_of_dependents'] = number_of_dependents

        self.table.update(ds)

    def delete(self, key: str):
        self.table.delete(ds)


    def __getitem__(self, key: str) -> DataRow:
        return self.collection.find_one({'_id': ObjectId(key)})


class PersonGateway:
    collection = 'Person'

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def get(self):
        pass
