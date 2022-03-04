from .abstract import AbstractRepository


class DynamoDBRepository(AbstractRepository):
    def __init__(self, boto3_dynamodb_client):
        self.boto3_dynamodb_client = boto3_dynamodb_client

    def get(self):
        pass

    def add(self):
        pass
