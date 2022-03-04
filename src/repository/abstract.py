import abc


class AbstractRepository(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def add(self):
        raise NotImplementedError()
