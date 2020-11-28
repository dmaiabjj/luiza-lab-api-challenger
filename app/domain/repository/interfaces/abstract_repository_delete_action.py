import abc
from abc import abstractmethod


class AbstractRepositoryDeleteAction(abc.ABC):
    @abstractmethod
    def delete(self, entity):
        raise NotImplementedError
