from pymongo.cursor import Cursor
from bson import (ObjectId)
from mongodb import (DatabaseClient, MONGO_DATABASE)


class PersonGateway:
    last_name: str
    first_name: str
    number_of_dependents: int
    collection = 'people'

    def __init__(self):
        self.db = DatabaseClient()[MONGO_DATABASE][self.collection]

    def set_last_name(self, last_name: str):
        self.last_name = last_name

    def get_last_name(self):
        return self.last_name

    def set_first_name(self, first_name: str):
        self.first_name = first_name

    def get_first_name(self):
        return self.first_name

    def set_number_of_dependents(self, number_of_dependents: int):
        self.number_of_dependents = number_of_dependents

    def get_number_of_dependents(self):
        return self.number_of_dependents

    property(get_last_name, set_last_name)
    property(get_first_name, set_first_name)
    property(get_number_of_dependents, set_number_of_dependents)

    def prepare_data(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'number_of_dependents': self.number_of_dependents
        }

    def prepare_update_data(self):
        return self.prepare_data()

    def update(self):
        update_data = self.prepare_update_data()
        self.db.update(update_data)

    def prepare_insert_data(self):
        prepared_data = self.prepare_data()
        prepared_data['_id'] = ObjectId()
        return prepared_data

    def insert(self):
        data_to_insert = self.prepare_insert_data()
        result = self.db.insert(data_to_insert)
        return result

    def load(self, rs: Cursor):
        data = list(rs)
        if not data:
            raise Exception('No data g')


class PersonFinder:
    def __init__(self):
        self.db = DatabaseClient()[MONGO_DATABASE][PersonGateway.collection]

    def find_query(self, _id: str):
        return {'_id': ObjectId(_id)}

    def find(self, _id: str):
        result: PersonGateway = Registry.get_person(_id)
        if result is not None:
            return result

        query = self.find_query(_id)
        rs = self.db.find(query)
        result = PersonGateway.load(rs)



