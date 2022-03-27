import pytest

from unittest.mock import Mock
from src.service.collection_service import CollectionService
from src.repository.memory import MemoryRepository


def test_collection_service_crud():
    mr = MemoryRepository(Mock())
    service = CollectionService(mr)

    assert service

    result = service.create_collection(name="Some name")
    assert result["uuid"]
    assert result["collection"] is not None
    assert result["collection"].name == "Some name"

    updated = service.rename_collection(uuid=result["uuid"], name="wow")
    assert updated["collection"].name == "wow"

    result2 = service.get_collections()

    item_uuid = service.add_item_to_collection(
        item_type="text", hint=["answer"], answer="bah", collection_uuid=result["uuid"]
    )

    service.update_item(item_uuid=item_uuid, item_type="text", hint=["buh"])

    assert len(result2) == 1
    assert result2[0][0] == result["uuid"]
    assert result2[0][1].name == "wow"
    assert result2[0][1].items[0].visible_side.get() == "buh"

    service.delete_collection(result["uuid"])
    assert len(service.get_collections()) == 0


@pytest.mark.skip
def test_collection_item_add():
    """Tests that different types of items don't throw errors"""

    mr = MemoryRepository(Mock())
    service = CollectionService(mr)

    uuid = service.create_collection("test")

    service.add_item_to_collection(
        answer="image_item",
        item_type="image",
        hint=["base64mock"],
        collection_uuid=uuid,
    )

    service.add_item_to_collection(
        answer="bah",
        item_type="multiple_choice",
        hint=["option1", "option2"],
        collection_uuid=uuid,
    )

    service.add_item_to_collection(
        hint=["bla ble ___ blo blu"],
        item_type="fillin",
        answer="bli",
        collection_uuid=uuid,
    )

    colls = service.get_collections()
    assert len(colls) == 3


def test_collection_iteration():
    """Tests that different types of items don't throw errors"""
    mr = MemoryRepository(Mock())
    service = CollectionService(mr)
    result = service.create_collection(name="Some name")
    uuid = result["uuid"]

    service.add_item_to_collection(
        hint=["bah"], item_type="text", answer="answer", collection_uuid=uuid
    )

    item = service.get_next_collection_item(collection_uuid=uuid)
    assert item

    service.give_feedback_to_item(collection_uuid=uuid, feedback="E")


def test_statistics_service():
    mr = MemoryRepository(Mock())
    service = CollectionService(mr)
    result = service.create_collection(name="Some name")
    statistics = service.get_collection_statistics(result["uuid"])
    assert statistics


def test_suggestion_service():
    mr = MemoryRepository(Mock())
    service = CollectionService(mr)
    result = service.create_collection(name="Some name")
    uuid = result["uuid"]

    service.add_item_to_collection(
        name="bah", item_type="text", answer=["answer"], collection_uuid=uuid
    )

    suggestion = service.suggest(uuid)
    assert suggestion["uuid"] == uuid
