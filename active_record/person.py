from pymongo.cursor import (Cursor)
from typing import Dict
from bson import (ObjectId)
from mongodb import (DatabaseClient, MONGO_DATABASE)
from revenue_revognition_problem.value_objects.money import Money


class Registry:
    __instances: {}
    collection = 'people'
    persons: Dict[Person]

    def __new__(cls, *args, **kwargs):
        """ For implementing Singleton object data pattern """
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Registry, cls).__new__(cls, *args, **kwargs)
        return cls.__instances[cls]

    def add_person(self, person: Person):
        self.persons.update({str(person.oid): person})

    def get_person(self, _id: str):
        return self.persons.get(_id)


class Person:
    last_name: str
    first_name: str
    number_of_dependents: int
    oid: ObjectId

    def __init__(self, _id=None, last_name=None, first_name=None, number_of_dependents=None):
        self.oid = _id
        self.last_name = last_name
        self.first_name = first_name
        self.number_of_dependents = number_of_dependents
        self.db = DatabaseClient()[MONGO_DATABASE][Registry.collection]

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
        data = list(rs)[0]
        _id: ObjectId = data['_id']
        first_name = data['first_name']
        last_name = data['last_name']
        number_of_dependents = data['number_of_dependents']

        result = Person(_id, last_name, first_name, number_of_dependents)
        Registry().add_person(result)
        return result

    def find_query(self, _id: str):
        return {'_id': ObjectId(_id)}

    def find(self, _id: str):
        result: Person = Registry().get_person(_id=_id)
        if result is not None:
            return result

        query = self.find_query(_id)
        rs = self.db.find(query)
        if rs.count() == 0:
            raise Exception('No person found with given id')
        result = Person().load(rs)

        return result

    def find_responsible_query(self):
        return {'number_of_dependents': {'$gt': 0}}, \
               {'first_name': 1, 'last_name': 1, 'number_of_dependents': 1}

    def find_responsibles(self):
        query_params = self.find_responsible_query()
        rs = self.db.find(*query_params)
        if rs.count() == 0:
            raise Exception('No person found with number_of_dependents more than 0')
        result = Person().load(rs)

        return result

    def get_exemption(self):
        base_exemption: Money = Money.dollars(1500)
        dependent_exemption:   Money = Money.dollars(750)
        return base_exemption.add(dependent_exemption.multiply(self.number_of_dependents))
