from src.repository.abstract import AbstractRepository
import src.domain as domain
from typing import List
from .errors import UnknownItemType

class CollectionService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def create_collection(self, name: str):
        col = domain.Collection()
        col.set_name(name)

        uuid = self.repository.collection_add(col)
        return {"uuid": uuid, "collection": col}

    def rename_collection(self, uuid: str, name: str):
        collection = self.repository.collection_get(uuid)
        collection.set_name(name)
        self.repository.collection_rename(uuid, name)
        return {"uuid": uuid, "collection": collection}

    def get_collections(self):
        return self.repository.collection_get_all()

    def add_item_to_collection(self, item_type: str, hint: List[str], answer: str, collection_uuid: str):
        i = domain.Item()
        i.set_answer(answer)
        self.set_item_type(i, item_type, hint)
        return self.repository.item_add(i, collection_uuid)

    def update_item(self, item_uuid: str, item_type: str = None, hint: List[str] = None, answer: str = None):
        item = self.repository.item_get(item_uuid)
        if item_type and hint:
            self.set_item_type(item, item_type, hint)
        self.repository.item_update(item_uuid, item)


    def set_item_type(self, i: domain.Item, item_type: str, hint: List[str]):
        upper_type = item_type.upper()
        if upper_type == "TEXT":
            i.set_text_type(hint[0])
        elif upper_type == "IMAGE":
            raise NotImplementedError()
        elif upper_type == "FILL_IN":
            i.set_fill_in_type(hint[0])
        elif upper_type == "MULTIPLE_CHOICES":
            i.set_multiple_choice_type(hint)
        else:
            raise UnknownItemType(item_type)

    def delete_collection(self, collection_uuid):
        self.repository.collection_get(collection_uuid)
        items = self.repository.item_get_all(collection_uuid)
        for item in items:
            self.repository.item_delete(item[0], collection_uuid)
        
        self.repository.collection_delete(collection_uuid)

    def get_next_collection_item(self):
        pass