import pytest

from src.controllers import collection_controller
from src.repository.memory import MemoryRepository
from src.service.collection_service import CollectionService


@pytest.fixture
def memory_repo():
    yield MemoryRepository(None)


@pytest.fixture
def collection_service(memory_repo):
    yield CollectionService(memory_repo)


def test_create_collection(collection_service):
    request = {"name": "bah"}
    response = collection_controller.create_collection(request, collection_service)
    assert response.status_code == 200
    assert response.body["uuid"]
    assert response.body["collection"]["name"] == "bah"
