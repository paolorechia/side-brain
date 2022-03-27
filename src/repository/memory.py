from .abstract import AbstractRepository
from .errors import ItemNotFound, CollectionNotFound, CollectionNotEmpty
from uuid import uuid4
import src.domain as domain
from typing import Dict, List, Tuple, Set


class MemoryRepository(AbstractRepository):
    def __init__(self, stub_adapter):
        self.stub_adapter = stub_adapter
        self.items: Dict[str, domain.Item] = {}
        self.collections: Dict[str, domain.Collection] = {}
        self.relationships: Dict[str, Set[str]] = {}

    def item_get(self, uuid: str) -> domain.Item:
        if uuid in self.items:
            return self.items[uuid]
        raise ItemNotFound()

    def item_add(self, item: domain.Item, collection_uuid: str) -> str:
        if not isinstance(item, domain.Item):
            raise TypeError()

        if collection_uuid not in self.collections:
            raise CollectionNotFound()

        new_id = str(uuid4())
        self.items[new_id] = item
        self.relationships[collection_uuid].add(new_id)
        return new_id

    def item_update(self, uuid: str, item: domain.Item):
        if uuid not in self.items:
            raise ItemNotFound()
        if not isinstance(item, domain.Item):
            raise TypeError()
        self.items[uuid] = item

    def item_get_all(self, collection_uuid: str) -> List[Tuple[str, domain.Item]]:
        result = []
        if collection_uuid not in self.relationships:
            raise CollectionNotFound()

        in_collection_uuids = self.relationships[collection_uuid]
        for key, item in self.items.items():
            if key in in_collection_uuids:
                result.append((key, item))
        return result

    def item_delete(self, uuid: str, collection_uuid: str) -> None:
        if collection_uuid not in self.relationships:
            raise CollectionNotFound()
        if uuid in self.items:
            del self.items[uuid]
            self.relationships[collection_uuid].remove(uuid)
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
        self.relationships[new_id] = set()
        return new_id

    def collection_rename(self, uuid: str, name: str):
        if not isinstance(name, str) or not name:
            raise TypeError()
        if uuid not in self.collections:
            raise CollectionNotFound()
        self.collections[uuid].name = name

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
