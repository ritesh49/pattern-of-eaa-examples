import pymongo

MONGO_URI = 'http://localhost:27017'
MONGO_DATABASE = 'revenue_recognition'


class MongoDB:
    """ Pymongo Wrapper class for executing mongo queries """
    __slots__ = '__db', '__collection', '__mongo_client', '__client'

    def __init__(self, database: str, collection: str):
        self.__db = database
        self.__collection = collection

        self.__mongo_client = pymongo.MongoClient(MONGO_URI)
        self.__client = self.__mongo_client[database][collection]

    def find_one(self, _filter=None, *args, **kwargs):
        return self.__client.find_one(_filter, *args, **kwargs)

    def find(self, *args, **kwargs):
        return self.__client.find(*args, **kwargs)

    def insert(self, doc_or_docs, manipulate=True,
               check_keys=True, continue_on_error=False, **kwargs):
        self.__client.insert(doc_or_docs, manipulate, check_keys, continue_on_error, **kwargs)


class CollectionClient:
    __slots__ = ('__db',) + MongoDB.__slots__

    def __init__(self, database: str):
        self.__db = database

    def __getitem__(self, collection: str):
        return MongoDB(database=self.__db, collection=collection)


class DatabaseClient:
    __slots__ = CollectionClient.__slots__ + MongoDB.__slots__

    def __getitem__(self, database: str):
        return CollectionClient(database=database)
