import abc
from abc import abstractmethod


class AbstractRepositoryCreateAction(abc.ABC):
    @abstractmethod
    def add(self, entity):
        raise NotImplementedError
