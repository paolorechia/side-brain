from .abstract import AbstractRepository


class DynamoDBRepository(AbstractRepository):
    def __init__(self, dynaborn_executor):
        self.dynaborn_executor = dynaborn_executor

    def get(self):
        pass

    def add(self):
        pass
