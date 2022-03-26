from src.repository.abstract import AbstractRepository


class CollectionService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository
