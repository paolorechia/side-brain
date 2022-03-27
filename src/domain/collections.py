import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple

import src.domain.errors as errors

from .items import Item, ItemFeedback, ItemStatistics, ItemClassificationType

RANDOM_NAMES = [
    "tuna",
    "whisky",
    "jar",
    "balloon",
    "name me plz",
    "who are you??" "pleeeease, give me a name!",
]

@dataclass
class CollectionStatistics:
    total_attempts: int = 0
    easy_answers: int = 0
    medium_answers: int = 0
    hard_answers: int = 0
    failed_answers: int = 0
    a_plus_items: int = 0
    a_items: int = 0
    b_items: int = 0
    c_items: int = 0
    d_items: int = 0
    e_items: int = 0


class Collection:
    def __init__(self):
        self.items: List[Item] = []
        self._db_items: List[Tuple[str, Item]] = []
        self.index = 0
        self.current = None
        self.name = random.choice(RANDOM_NAMES)

    def set_name(self, name: str):
        if not name:
            raise errors.InvalidCollectionName()
        if not isinstance(name, str):
            raise errors.InvalidCollectionName()

        self.name = name

    def get_statistics(self) -> CollectionStatistics:
        cstats = CollectionStatistics()
        for item in self.items:
            istats: ItemStatistics = item.get_statistics()
            cstats.total_attempts += istats.total_attempts
            cstats.easy_answers += istats.easy_answers
            cstats.medium_answers += istats.medium_answers
            cstats.hard_answers += istats.hard_answers
            cstats.failed_answers += istats.failed_answers
            if item.classification.type_ == ItemClassificationType.APLUS:
                cstats.a_plus_items += 1
            elif item.classification.type_ == ItemClassificationType.A:
                cstats.a_items += 1
            elif item.classification.type_ == ItemClassificationType.B:
                cstats.b_items += 1
            elif item.classification.type_ == ItemClassificationType.C:
                cstats.c_items += 1
            elif item.classification.type_ == ItemClassificationType.D:
                cstats.d_items += 1
            elif item.classification.type_ == ItemClassificationType.E:
                cstats.e_items += 1
        return cstats

    def shuffle(self):
        random.shuffle(self.items)

    def add(self, item: Item):
        if not item:
            raise errors.InvalidItemType()
        if not isinstance(item, Item):
            raise errors.InvalidItemType()

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

        if self.current.classification.type_ == current_classification:
            self.items.append(self.items.pop(self.index))
        else:
            self.index += 1

    def __len__(self) -> int:
        return len(self.items)
