from dataclasses import dataclass

import boto3
import moto
import pytest
from src.dynaborn import UUID, Column, Integer, String, Table, Executor, mapper


@dataclass
class SampleClass:
    abc: str
    number: int


@pytest.fixture
def table():
    yield Table(
        "test_table",
        Column("pk", UUID, auto_generate=True),
        Column("abc", String),
        Column("number", Integer),
    )


def test_dynaborn_table(table):
    assert table


def test_dynaborn_mapper(table):
    mapper(table, SampleClass)
    assert True


@pytest.fixture
def boto3_dynamodb_client():
    yield boto3.client("dynamodb")


def test_dynaborn_executor_create_table(boto3_dynamodb_client, table):
    dynaborn_executor = Executor(boto3_dynamodb_client)

    dynaborn_executor.create_table(table)


def test_dynaborn_executor_get_table(boto3_dynamodb_client):
    dynaborn_executor = Executor(boto3_dynamodb_client)

    dynaborn_executor.get_table(table)


def test_dynaborn_executor_delete_table(boto3_dynamodb_client):
    dynaborn_executor = Executor(boto3_dynamodb_client)

    dynaborn_executor.delete_table(table)


def test_dynaborn_executor_scan(boto3_dynamodb_client, table):
    dynaborn_executor = Executor(boto3_dynamodb_client)

    dynaborn_executor.table(table).scan()


def test_dynaborn_executor_get(boto3_dynamodb_client):
    dynaborn_executor = Executor(boto3_dynamodb_client)

    dynaborn_executor.table(table).get()


def test_dynaborn_executor_put(boto3_dynamodb_client):
    dynaborn_executor = Executor(boto3_dynamodb_client)

    dynaborn_executor.table(table).put()


def test_dynaborn_executor_delete(boto3_dynamodb_client):
    dynaborn_executor = Executor(boto3_dynamodb_client)

    dynaborn_executor.table(table).delete()
