from typing import List, Tuple

import src.domain as domain

from .abstract import AbstractRepository


class DynamoDBRepository(AbstractRepository):
    def __init__(self, boto3_dynamodb_client):
        self.ddb_client = boto3_dynamodb_client

    def item_get(self, uuid: str) -> domain.Item:
        raise NotImplementedError()

    def item_add(self, item: domain.Item, collection_uuid: str) -> str:
        return ""

    def item_update(self, uuid: str, item: domain.Item) -> None:
        pass

    def item_get_all(self, collection_uuid: str) -> List[Tuple[str, domain.Item]]:
        return []

    def item_delete(self, uuid: str, collection_uuid: str) -> None:
        pass

    def collection_get(self, uuid: str) -> domain.Collection:
        raise NotImplementedError()

    def collection_add(self, collection: domain.Collection) -> str:
        return ""

    def collection_rename(self, uuid: str, name: str):
        pass

    def collection_update_index(self, uuid: str, index: int):
        pass

    def collection_get_all(self) -> List[Tuple[str, domain.Collection]]:
        return []

    def collection_delete(self, uuid: str) -> None:
        pass

    def upload_image(self, binary: bytes) -> str:
        pass
