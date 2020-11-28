import abc
from abc import abstractmethod


class AbstractRepositoryReadAction(abc.ABC):
    @abstractmethod
    def find_by_id(self, id):
        raise NotImplementedError
