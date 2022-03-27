import pytest
import boto3
from unittest.mock import Mock

import src.domain as domain
from src.repository.memory import MemoryRepository
from src.repository.errors import ItemNotFound, CollectionNotFound, CollectionNotEmpty


def test_memory_repository_exists():
    r = MemoryRepository(Mock())
    assert r


def test_memory_repository_collection_ops():
    r = MemoryRepository(Mock())

    c = domain.Collection()
    c2 = domain.Collection()

    uuid_1 = r.collection_add(c)

    c2 = r.collection_get(uuid_1)

    assert c == c2

    uuid_2 = r.collection_add(domain.Collection())

    c3 = r.collection_get(uuid_2)

    collection_list = r.collection_get_all()

    assert len(collection_list) == 2
    ids_ = [i[0] for i in collection_list]
    assert uuid_1 in ids_
    assert uuid_2 in ids_

    r.collection_delete(uuid_1)

    collection_list = r.collection_get_all()

    assert len(collection_list) == 1
    colls = [i[1] for i in collection_list]
    assert c not in colls
    assert c3 in colls


def test_memory_repository_collection_errors():
    r = MemoryRepository(Mock())

    with pytest.raises(TypeError):
        r.collection_add(domain.Item())

    with pytest.raises(TypeError):
        r.collection_rename("a", None)

    with pytest.raises(CollectionNotFound):
        r.collection_get("a")

    with pytest.raises(CollectionNotFound):
        r.collection_delete("b")

    with pytest.raises(CollectionNotFound):
        r.collection_rename("c", "d")

    c = domain.Collection()
    i = domain.Item()
    c.add(i)
    uuid_ = r.collection_add(c)

    with pytest.raises(CollectionNotEmpty):
        r.collection_delete(uuid_)


def test_memory_repository_item_ops():
    r = MemoryRepository(Mock())

    c = domain.Collection()

    col_uuid = r.collection_add(c)

    i = domain.Item()
    i2 = domain.Item()

    uuid_1 = r.item_add(i, col_uuid)

    i2 = r.item_get(uuid_1)

    assert i == i2

    uuid_2 = r.item_add(domain.Item(), col_uuid)

    updated = domain.Item()
    r.item_update(uuid_2, updated)

    i3 = r.item_get(uuid_2)

    item_list = r.item_get_all(col_uuid)

    assert len(item_list) == 2
    ids_ = [i[0] for i in item_list]
    assert uuid_1 in ids_
    assert uuid_2 in ids_

    r.item_delete(uuid_1, col_uuid)

    item_list = r.item_get_all(col_uuid)

    assert len(item_list) == 1
    items = [i[1] for i in item_list]
    assert i not in items
    assert i3 in items


def test_memory_repository_item_errors():
    r = MemoryRepository(Mock())

    with pytest.raises(TypeError):
        r.item_add(domain.Collection(), "c")

    with pytest.raises(CollectionNotFound):
        r.item_get_all("b")

    with pytest.raises(CollectionNotFound):
        r.item_add(domain.Item(), "b")

    with pytest.raises(CollectionNotFound):
        r.item_delete(domain.Item(), "b")

    with pytest.raises(ItemNotFound):
        r.item_get("a")

    with pytest.raises(ItemNotFound):
        r.item_update("a", domain.Item())

    with pytest.raises(ItemNotFound):
        cuuid = r.collection_add(domain.Collection())
        r.item_delete("b", cuuid)

    with pytest.raises(TypeError):
        cuuid = r.collection_add(domain.Collection())
        uuid = r.item_add(domain.Item(), cuuid)
        r.item_update(uuid, "asd")


def test_memory_repository_item_collection_separation():
    r = MemoryRepository(Mock())

    c = domain.Collection()
    c2 = domain.Collection()

    col_uuid = r.collection_add(c)
    col_uuid2 = r.collection_add(c2)

    i = domain.Item()
    i2 = domain.Item()
    i3 = domain.Item()
    i4 = domain.Item()

    uuid1 = r.item_add(i, col_uuid)
    uuid2 = r.item_add(i2, col_uuid)

    r.item_add(i3, col_uuid)

    r.item_add(i4, col_uuid2)

    assert len(r.item_get_all(col_uuid)) == 3
    assert len(r.item_get_all(col_uuid2)) == 1
