from bson import ObjectId
from typing import List
from abc import ABC, abstractmethod
from mongodb import DatabaseClient as DB, MONGO_DATABASE


class Person:
    collection = 'person'

    last_name: str
    first_name: str
    number_of_dependents: int
    oid: ObjectId

    def __init__(self, _id=None, last_name=None, first_name=None, number_of_dependents=None):
        self.oid = _id
        self.last_name = last_name
        self.first_name = first_name
        self.number_of_dependents = number_of_dependents

    @property
    def data(self):
        return {
            '_id': self.oid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'number_of_dependents': self.number_of_dependents
        }


"""
Db collection schema
{
    "first_name": "Ritesh",
    "last_name": "Ramchandani",
    "number_of_dependents": 10
}
"""


class StatementSource(ABC):
    query: dict

    @abstractmethod
    @property
    def prepare_query(self):
        pass

    @abstractmethod
    @property
    def parameters(self):
        pass


class AbstractMapper(ABC):
    _projection: str
    loaded_map = dict()

    def __init__(self):
        self.db = DB()[MONGO_DATABASE][Person.collection]

    @abstractmethod
    def _prepare_find_query(self, _id: str) -> dict:
        pass

    @abstractmethod
    def _prepare_find_by_last_name_query(self, last_name) -> dict:
        pass

    @abstractmethod
    def prepare_update_query(self, _id: str, subject: Person) -> tuple:
        pass

    def do_load(self, _id: str, rs: ResultSet):
        last_name: str = rs['last_name']
        first_name: str = rs['first_name']
        num_dependents: int = rs['number_of_dependents']
        return Person(_id, last_name, first_name, num_dependents)

    def load(self, rs: ResultSet):
        _id = rs['_id']
        if self.loaded_map.__contains__(_id):
            return self.loaded_map.get(_id)
        result: DomainObject = self.do_load(_id, rs)
        self.loaded_map.update({_id: result})
        return result

    def load_all(self, rs: ResultSet):
        result: List[Person] = list()
        for result_set in rs:
            result.append(self.load(result_set))
        return result

    def _abstract_find(self, _id: str):
        result: DomainObject = self.loaded_map.get(_id)
        if result:
            return result
        find_query = self._prepare_find_query(_id)
        rs: ResultSet = self.db.find(find_query, self._projection)
        result = self.load(rs)
        return result

    def _insert(self, subject: DomainSubject):
        pass


class PersonMapper(AbstractMapper):
    projection = {'_id': 1, 'first_name': 1, 'last_name': 1,'number_of_dependents': 1}

    def _prepare_find_query(self, _id: str) -> dict:
        return {'_id': ObjectId(_id)}

    def find(self, _id: str) -> Person:
        return self._abstract_find(_id)

    def _prepare_find_by_last_name_query(self, last_name):
        return {'last_name': last_name}

    def find_by_last_name(self, last_name: str):
        find_query = self._prepare_find_by_last_name_query(last_name)
        rs: ResultSet = self.db.find(find_query, self.projection)
        return self.load_all(rs)

    def find_many(self, source: StatementSource):
        """
            generalized find method for all cases
        """
        find_query = source.prepare_query  # prepare query will prepare using source.parameters which'l have person dtls
        rs: ResultSet = self.db.find(find_query, self.projection)
        return self.load_all(rs)

    def find_by_last_name_v2(self, pattern: str):
        """
            Version 2 of find_by_last_name
            using inner class FindByLastName for wrapping mongo queries
        """
        return self.find_many(self.FindByLastName(pattern))

    def _prepare_update_query(self, _id: str, subject: Person) -> tuple:
        return {'_id': ObjectId(_id)}, {'$set': {**subject}}

    def update(self, _id: str, subject: Person):
        update_query = self._prepare_update_query(_id, subject)
        self.db.update(*update_query)

    def _insert(self, abs_subject: DomainSubject):
        # https://medium.com/swlh/dont-use-database-generated-ids-d703d35e9cc4
        # blog for sharing why oid is generated here
        subject: Person = abs_subject
        subject.oid = ObjectId()
        subject.first_name = subject.first_name
        subject.last_name = subject.last_name
        subject.number_of_dependents = subject.number_of_dependents
        self.db.insert(subject.data)

    class FindByLastName(StatementSource):
        last_name: str

        def __init__(self, last_name: str):
            self.last_name = last_name

        def prepare_query(self):
            params = self.parameters()
            return {'last_name': params[0]}

        def parameters(self):
            return [self.last_name]


