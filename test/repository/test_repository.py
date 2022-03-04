import pytest
import boto3

from src.repository.dynamodb import DynamoDBRepository


@pytest.fixture
def boto3_dynamodb_client():
    yield boto3.client("dynamodb")


def test_dynamodb_repository_exists(boto3_dynamodb_client):
    r = DynamoDBRepository(boto3_dynamodb_client)
    assert r
