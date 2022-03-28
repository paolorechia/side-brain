import pytest

from src.controllers import collection_controller
from src.controllers.request import HTTPMethod, Request


def test_create_collection(collection_service):
    request = Request(
        resource="/collection", method=HTTPMethod.POST, body={"name": "bah"}
    )


def test_rename_collection(collection_service):
    request = Request(
        resource="/",
        method=HTTPMethod.PATCH,
        path_parameters={"collection": uuid},
        body={"name": "renamed"},
    )


def test_get_collections(collection_service):
    request = Request(resource="/collection", method=HTTPMethod.GET)


def test_add_item_to_collection(collection_service):
    request = Request(
        resource="/item",
        method=HTTPMethod.POST,
        path_parameters={"collection": uuid},
        body={
            "item_type": "text",
            "hint": ["Lovely"],
            "answer": "Or not",
        },
    )


def test_update_item(collection_service):
    request = Request(
        resource="/item",
        method=HTTPMethod.POST,
        path_parameters={"collection": uuid},
        body={
            "hint": ["Lovely2"],
        },
    )


def test_delete_collection(collection_service):
    pass


def test_get_next_collection_item(collection_service):
    pass


def test_give_feedback_to_item(collection_service):
    pass


def test_get_collection_statistics(collection_service):
    pass


def test_suggest(collection_service):
    pass
