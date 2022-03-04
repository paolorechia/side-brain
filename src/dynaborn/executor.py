from .table import Table


class Executor:
    def __init__(self, boto3_dynamodb_client):
        pass

    def create_table(self, table: Table):
        pass

    def get_table(self, table: Table):
        pass

    def delete_table(self, table: Table):
        pass

    def table(self, table: Table):
        return _TableExecutor(table)


class _TableExecutor:
    def __init__(self, table: Table):
        self.table = Table
        pass

    def scan(self):
        pass

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
