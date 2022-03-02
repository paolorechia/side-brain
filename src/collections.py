from .items import Item
from typing import Optional


class Collection:
    def __init__(self):
        self.items = []

    def add(self, item: Item):
        self.items.append(item)

    def next(self) -> Optional[Item]:
        return None

    def __len__(self) -> int:
        return len(self.items)
