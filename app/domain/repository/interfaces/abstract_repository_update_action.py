import abc
from abc import abstractmethod


class AbstractRepositoryUpdateAction(abc.ABC):
    @abstractmethod
    def update_from_dict(self, entity, data):
        raise NotImplementedError

    @abstractmethod
    def update_from_model(self, entity, data):
        raise NotImplementedError
