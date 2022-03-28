from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class CreateCollectionCommand:
    name: str


@dataclass(frozen=True)
class RenameCollectionCommand:
    uuid: str
    name: str


class GetAllCollectionsCommand:
    def __init__(self):
        pass


@dataclass(frozen=True)
class AddItemToCollectionCommand:
    item_type: str
    hint: List[str]
    answer: str
    collection_uuid: str


@dataclass(frozen=True)
class UpdateItemCommand:
    item_uuid: str
    item_type: Optional[str] = None
    hint: Optional[List[str]] = None
    answer: Optional[str] = None


@dataclass(frozen=True)
class DeleteCollectionCommand:
    collection_uuid: str


@dataclass(frozen=True)
class GetNextCollectionItemCommand:
    collection_uuid: str


@dataclass(frozen=True)
class GiveFeedbackToItemCommand:
    collection_uuid: str
    feedback_str: str


@dataclass(frozen=True)
class GetCollectionStatisticsCommand:
    collection_uuid: str


class SuggestCommand:
    def __init__(self):
        pass
