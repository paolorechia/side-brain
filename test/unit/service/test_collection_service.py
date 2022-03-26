import pytest

from unittest.mock import Mock
from src.service.collection import CollectionService
from src.repository.memory import MemoryRepository


def test_collection_service():
    mr = MemoryRepository(Mock())
    service = CollectionService(mr)

    assert service
