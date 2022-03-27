from src.repository.abstract import AbstractRepository
import src.domain as domain
from typing import List
from .errors import UnknownItemType, FailedToGiveFeedback
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
        logger.info("Adding item: %s to collection (%s)", i, collection_uuid)
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
            link = self.repository.upload_image(hint[0])
            i.set_image_type(link)
        elif upper_type == "FILL_IN":
            i.set_fill_in_type(hint[0])
        elif upper_type == "MULTIPLE_CHOICE":
            i.set_multiple_choice_type(hint)
        else:
            raise UnknownItemType(item_type)

    def delete_collection(self, collection_uuid: str):
        self.repository.collection_get(collection_uuid)
        items = self.repository.item_get_all(collection_uuid)
        for item in items:
            self.repository.item_delete(item[0], collection_uuid)
        
        self.repository.collection_delete(collection_uuid)

    def get_next_collection_item(self, collection_uuid: str):
        logger.info("Getting next collection item: %s", collection_uuid)
        collection = self.repository.collection_get(collection_uuid)
        next_ = collection.next()
        logger.info("Current collection index: %s", collection.index)
        self.repository.collection_update_index(collection_uuid, collection.index)
        return next_

    def give_feedback_to_item(self, collection_uuid: str, feedback: str):
        if not isinstance(feedback, str) or not feedback:
            raise TypeError()
        upper_feedback = feedback.upper()

        enum_feedback = domain.ItemFeedback(upper_feedback)

        collection = self.repository.collection_get(collection_uuid)
        collection.answer_item(enum_feedback)

        item = collection.current

        # Get DB relationship
        # Database details are leaking into the model here
        # Not ideal, but fixing it would require a major rework
        try:
            current_uuid = collection._db_items[collection.index - 1][0]
        except IndexError:
            raise FailedToGiveFeedback()

        logger.info("Updating feedback on item: %s", current_uuid)
        self.repository.item_update(current_uuid, item)  # Use UUID

    def get_collection_statistics(self, uuid: str):
        col = self.repository.collection_get(uuid)
        return col.get_statistics()

    def suggest(self):
        tuples = self.repository.collection_get_all()
        suggestions = domain.Suggestions()
        for t in tuples:
            suggestions.add(t[1])
        
        return suggestions.suggest()
