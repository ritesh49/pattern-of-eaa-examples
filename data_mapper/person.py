from bson import ObjectId
from abc import ABC, abstractmethod
from mongodb import DatabaseClient as DB, MONGO_DATABASE


class Person:
    collection = 'person'

    last_name: str
    first_name: str
    number_of_dependents: int


"""
Db collection schema
{
    "first_name": "Ritesh",
    "last_name": "Ramchandani",
    "number_of_dependents": 10
}
"""


class AbstractMapper(ABC):
    _projection: str
    loaded_map = dict()

    def __init__(self):
        self.db = DB()[MONGO_DATABASE][Person.collection]

    @abstractmethod
    def _prepare_find_query(self, _id: str) -> dict:
        pass

    @abstractmethod
    def do_load(self, _id: str, rs: ResultSet):
        pass

    def load(self, rs: ResultSet):
        _id = rs['_id']
        if self.loaded_map.__contains__(_id):
            return self.loaded_map.get(_id)
        result: DomainObject = self.do_load(_id, rs)
        self.loaded_map.update({_id: result})
        return result

    def _abstract_find(self, _id: str):
        result: DomainObject = self.loaded_map.get(_id)
        if result:
            return result
        find_query = self._prepare_find_query(_id)
        rs: ResultSet = self.db.find(find_query, self._projection)
        result = self.load(rs)
        return result


class PersonMapper:
    projection = {'_id': 1, 'first_name': 1, 'last_name': 1,'number_of_dependents': 1}

    def prepare_find_query(self, _id: str) -> dict:
        return {'_id': ObjectId(_id)}

    def find(self, _id: str) -> Person:
        return self.abstract_find(_id)



