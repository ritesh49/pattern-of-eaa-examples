"""
    This shows table data gateway using simple gateway class
"""
from bson import ObjectId

from mongodb import DatabaseClient, MONGO_DATABASE
from exceptions import InvalidMongoFilter, InvalidMongoKey


class DataReader:
    pass


class PersonGateway:
    def __init__(self):
        self.db_client = DatabaseClient()
        self.collection = 'person'
        self.db = MONGO_DATABASE + '_dependants'
        self.person_client = self.db_client[self.db][self.collection]

    def find_all(self) -> DataReader:
        return self.person_client.find()

    def find_with_last_name(self, last_name: str) -> DataReader:
        return self.person_client.find({'last_name': last_name})

    def find_with_filter(self, filters: dict) -> DataReader:
        if not isinstance(filters, dict):
            raise InvalidMongoFilter(f'Invalid Mongo filters passed in query {filters}')
        return self.person_client.find(filters)

    def find_row(self, key: ObjectId) -> DataReader:
        if not isinstance(key, ObjectId):
            raise InvalidMongoKey(f'Invalid mongo key passed for query {key}')
        return self.person_client.find({'_id': key})

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
