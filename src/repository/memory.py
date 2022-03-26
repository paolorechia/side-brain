from .abstract import AbstractRepository
from .errors import ItemNotFound, CollectionNotFound, CollectionNotEmpty
from uuid import uuid4
import src.domain as domain
from typing import Dict, List, Tuple


class MemoryRepository(AbstractRepository):
    def __init__(self, stub_adapter):
        self.stub_adapter = stub_adapter
        self.items: Dict[str, domain.Item] = {}
        self.collections: Dict[str, domain.Collection] = {}

    def item_get(self, uuid: str) -> domain.Item:
        if uuid in self.items:
            return self.items[uuid]
        raise ItemNotFound()

    def item_add(self, item: domain.Item) -> str:
        if not isinstance(item, domain.Item):
            raise TypeError()

        new_id = str(uuid4())
        self.items[new_id] = item
        return new_id

    def item_get_all(self) -> List[Tuple[str, domain.Item]]:
        result = []
        for key, item in self.items.items():
            result.append((key, item))
        return result

    def item_delete(self, uuid: str) -> None:
        if uuid in self.items:
            del self.items[uuid]
            return
        raise ItemNotFound()

    def collection_get(self, uuid: str) -> domain.Collection:
        if uuid in self.collections:
            return self.collections[uuid]
        raise CollectionNotFound()

    def collection_add(self, collection: domain.Collection) -> str:
        if not isinstance(collection, domain.Collection):
            raise TypeError()

        new_id = str(uuid4())
        self.collections[new_id] = collection
        return new_id

    def collection_get_all(self) -> List[Tuple[str, domain.Collection]]:
        result = []
        for key, item in self.collections.items():
            result.append((key, item))
        return result

    def collection_delete(self, uuid: str) -> None:
        if uuid in self.collections:
            if len(self.collections[uuid].items) > 0:
                raise CollectionNotEmpty()
            del self.collections[uuid]
            return
        raise CollectionNotFound()
