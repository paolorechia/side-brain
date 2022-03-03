from .items import Item, ItemFeedback
from typing import Optional, List
import src.errors as errors
from datetime import datetime
import random


class Collection:
    def __init__(self):
        self.items: List[Item] = []
        self.index = 0
        self.current = None

    def shuffle(self):
        random.shuffle(self.items)

    def add(self, item: Item):
        self.items.append(item)

    def next(self) -> Optional[Item]:
        if not self.items:
            return None

        if self.index >= len(self.items):
            self.index = 0
            self.current = None
            return None

        self.current = self.items[self.index]
        while self.current.wait_until > datetime.now():
            self.index += 1

            if self.index >= len(self.items):
                self.index = 0
                self.current = None
                return None

        return self.current

    def answer_item(self, feedback: ItemFeedback):
        if not feedback or not isinstance(feedback, ItemFeedback):
            raise errors.InvalidItemFeedback()
        if not self.current:
            raise errors.NoItemToAnswerException()

        current_classification = self.current.classification.type_
        self.current.push_feedback(feedback)
        self.index += 1
        if self.current.classification.type_ == current_classification:
            self.items.append(self.current)

    def __len__(self) -> int:
        return len(self.items)
