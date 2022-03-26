import abc
import src.domain as domain
from typing import List, Tuple


class AbstractRepository(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def item_get(self, uuid: str) -> domain.Item:
        raise NotImplementedError()

    @abc.abstractmethod
    def item_add(self, item: domain.Item) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def item_get_all(self) -> List[Tuple[str, domain.Item]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def item_delete(self, uuid: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def collection_get(self, uuid: str) -> domain.Collection:
        raise NotImplementedError()

    @abc.abstractmethod
    def collection_add(self, collection: domain.Collection) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def collection_get_all(self) -> List[Tuple[str, domain.Collection]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def collection_delete(self, uuid: str) -> None:
        raise NotImplementedError()
