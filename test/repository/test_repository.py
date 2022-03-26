import pytest
import boto3
from unittest.mock import Mock

import src.domain as domain
from src.repository.dynamodb import DynamoDBRepository
from src.repository.memory import MemoryRepository


@pytest.fixture
def boto3_dynamodb_client():
    yield boto3.client("dynamodb")


def test_dynamodb_repository_exists(boto3_dynamodb_client):
    r = DynamoDBRepository(boto3_dynamodb_client)
    assert r


def test_memory_repository_exists():
    r = MemoryRepository(Mock())
    assert r


def test_memory_repository_item_ops():
    r = MemoryRepository(Mock())
    i = domain.Item()
    i2 = domain.Item()

    uuid_1 = r.item_add(i)

    i2 = r.item_get(uuid_1)

    assert i == i2

    uuid_2 = r.item_add(domain.Item())

    i3 = r.item_get(uuid_2)

    item_list = r.item_get_all()

    assert len(item_list) == 2
    ids_ = [i[0] for i in item_list]
    assert uuid_1 in ids_
    assert uuid_2 in ids_

    r.item_delete(uuid_1)

    item_list = r.item_get_all()

    assert len(item_list) == 1
    items = [i[1] for i in item_list]
    assert i not in items
    assert i3 in items
