import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import src.errors as errors

from .items import Item, ItemFeedback


@dataclass
class CollectionStatistics:
    total_attempts: int
    easy_answers: int
    medium_answers: int
    hard_answers: int
    failed_answers: int
    a_plus_items: int
    a_items: int
    b_items: int
    c_items: int
    d_items: int
    e_items: int


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
