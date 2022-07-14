from abc import ABC, abstractmethod
from mongodb import DatabaseClient as DB, MONGO_DATABASE


class Artist:
    collection = 'artist'


class ArtistFinder(ABC):
    """
        Artist finder interface is connected with Domain object
        So, domain interacts with interface methods which can be replaced by actual classes in functn params
    """

    @abstractmethod
    def find(self, _id: str) -> Artist:
        pass


class ArtistMapper(ArtistFinder):
    """
        Actual implementation of separated interface(ArtistFinder)
    """
    def find(self, _id: str) -> Artist:
        return self._abstract_find(_id)


class AbstractMapper(ABC):
    _projection: str
    loaded_map = dict()

    def __init__(self):
        self.db = DB()[MONGO_DATABASE][Artist.collection]

    @abstractmethod
    def _prepare_find_query(self, _id: str) -> dict:
        pass

