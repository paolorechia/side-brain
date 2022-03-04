import pytest
import boto3

from src.repository.dynamodb import DynamoDBRepository
from src.dynaborn import Executor


@pytest.fixture
def boto3_dynamodb_client():
    yield boto3.client("dynamodb")


@pytest.fixture
def dynaborn_executor(boto3_dynamodb_client):
    yield Executor(boto3_dynamodb_client)


def test_dynamodb_repository_exists(dynaborn_executor):
    r = DynamoDBRepository(dynaborn_executor)
    assert r
