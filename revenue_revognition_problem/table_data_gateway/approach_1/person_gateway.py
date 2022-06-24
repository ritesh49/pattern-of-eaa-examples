"""
    This shows table data gateway using simple gateway class
"""
from bson import ObjectId
from pymongo.cursor import Cursor
from typing import Optional, List, Dict

from ..mongodb import DatabaseClient, MONGO_DATABASE
from ..exceptions import InvalidMongoFilter, InvalidMongoKey


class DataReader:
    def __init__(self, db_name: str):
        self._db_name = db_name
        self.__data = None

    def fill_data(self, data: Cursor):
        pass

    @property
    def data(self) -> Optional[List, Dict]:
        return self.__data


class PersonGateway:
    def __init__(self):
        self.db_client = DatabaseClient()
        self.collection = 'person'
        self.db = MONGO_DATABASE + '_dependants'
        self.person_client = self.db_client[self.db][self.collection]

    def find_all(self) -> DataReader:
        return self.person_client.find()

    def find_with_last_name(self, last_name: str) -> DataReader:
        data = self.person_client.find({'last_name': last_name})
        data_reader = self.__init_data_reader(data)
        return data_reader

    def find_with_filter(self, filters: dict) -> DataReader:
        if not isinstance(filters, dict):
            raise InvalidMongoFilter(f'Invalid Mongo filters passed in query {filters}')
        data = self.person_client.find(filters)
        data_reader = self.__init_data_reader(data)
        return data_reader

    def find_row(self, key: ObjectId) -> DataReader:
        if not isinstance(key, ObjectId):
            raise InvalidMongoKey(f'Invalid mongo key passed for query {key}')

        data = self.person_client.find({'_id': key})
        data_reader = self.__init_data_reader(data)
        return data_reader

    def update(self, key: ObjectId, last_name: str, first_name: str, number_of_dependents: int):
        if not isinstance(key, ObjectId):
            raise InvalidMongoKey(f'Invalid mongo key passed for query {key}')
        return self.person_client.update({'_id': key}, {'$set': {'last_name': last_name, 'first_name': first_name,
                                                                 'number_of_dependents': number_of_dependents}})

    def insert(self, last_name: str, first_name: str, number_of_dependents: int):
        self.person_client.insert({'last_name': last_name, 'first_name': first_name,
                                   'number_of_dependents': number_of_dependents})

    def delete(self, key: ObjectId):
        return self.person_client.delete({'_id': key})

    def __init_data_reader(self, data):
        data_reader = DataReader(self.collection)
        data_reader.fill_data(data=data)
        return data_reader
