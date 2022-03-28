import pytest

from src.controllers import collection_controller
from src.controllers.request import HTTPMethod, Request
from src.domain import commands
from src.repository.memory import MemoryRepository
from src.service.collection_service import CollectionService


@pytest.fixture
def memory_repo():
    yield MemoryRepository(None)


@pytest.fixture
def collection_service(memory_repo):
    yield CollectionService(memory_repo)


def test_create_collection(collection_service):
    response = collection_controller.invoke(
        commands.CreateCollectionCommand(name="duh"), collection_service
    )
    assert response.status_code == 201
    assert response.body["uuid"]


def test_rename_collection(collection_service):
    uuid = collection_service.create_collection("heh")["uuid"]
    response = collection_controller.invoke(
        commands.RenameCollectionCommand(uuid=uuid, name="renamed"), collection_service
    )
    assert response.status_code == 200
    assert response.body["uuid"] == uuid


def test_get_collections(collection_service):
    uuid = collection_service.create_collection("heh")["uuid"]
    uuid2 = collection_service.create_collection("heh2")["uuid"]
    uuid3 = collection_service.create_collection("heh3")["uuid"]
    response = collection_controller.invoke(
        commands.GetAllCollectionsCommand, collection_service
    )

    assert response.status_code == 200
    assert len(response.body["items"]) == 3
    first = response.body["items"]
    first["collection"]["name"] == "heh"
    first["uuid"] = uuid


def test_add_item_to_collection(collection_service):
    uuid = collection_service.create_collection("heh")["uuid"]
    response = collection_controller.invoke(
        commands.AddItemToCollectionCommand("text", ["Lovely"], "Or not", uuid),
        collection_service,
    )
    assert response.status_code == 201
    assert response.body["uuid"]


def test_update_item(collection_service):
    uuid = collection_service.create_collection("heh")["uuid"]
    item_uuid = collection_service.add_item_to_collection(
        "text", hint=["Test"], answer="ohno", uuid=uuid
    )

    response = collection_controller.invoke(
        commands.UpdateItemCommand(
            item_uuid=item_uuid, item_type=item_type, hint=["Lovely2"], answer="ohno"
        ),
        collection_service,
    )
    assert response.status_code == 200


def test_delete_collection(collection_service):
    uuid = collection_service.create_collection("heh")["uuid"]
    response = collection_controller.invoke(
        commands.DeleteCollectionCommand(uuid), collection_service
    )
    assert response.status_code == 200


def test_get_next_collection_item(collection_service):
    uuid = collection_service.create_collection("heh")["uuid"]
    response = collection_controller.invoke(
        commands.AddItemToCollectionCommand("text", ["Lovely"], "Or not", uuid),
        collection_service,
    )

    response = collection_controller.invoke(
        commands.GetNextCollectionItemCommand(uuid), collection_service
    )
    assert response.status_code == 200


def test_give_feedback_to_item(collection_service):
    uuid = collection_service.create_collection("heh")["uuid"]
    response = collection_controller.invoke(
        commands.GiveFeedbackToItemCommand(uuid, "HARD"), collection_service
    )
    assert response.status_code == 200


def test_get_collection_statistics(collection_service):
    uuid = collection_service.create_collection("heh")["uuid"]
    response = collection_controller.invoke(
        commands.GetCollectionStatisticsCommand(), collection_service
    )
    assert response.status_code == 200


def test_suggest(collection_service):
    response = collection_controller.invoke(
        commands.SuggestCommand(), collection_service
    )
    assert response.status_code == 200
