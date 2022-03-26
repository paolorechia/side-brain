from .abstract import AbstractRepository
from .errors import ItemNotFound
from uuid import uuid4
import src.domain as domain
from typing import Dict, List, Tuple


class MemoryRepository(AbstractRepository):
    def __init__(self, stub_adapter):
        self.stub_adapter = stub_adapter
        self.items: Dict[str, domain.Item] = {}
        self.collections: Dict[str, domain.Collection] = {}

    def item_add(self, item: domain.Item) -> str:
        new_id = str(uuid4())
        self.items[new_id] = item
        return new_id

    def item_get(self, uuid: str) -> domain.Item:
        if uuid in self.items:
            return self.items[uuid]
        raise ItemNotFound()

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
        raise NotImplementedError()

    def collection_add(self, collection: domain.Collection) -> str:
        return ""

    def collection_get_all(self) -> List[Tuple[str, domain.Collection]]:
        return []

    def collection_delete(self, uuid: str) -> None:
        pass
