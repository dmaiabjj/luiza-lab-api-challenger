import abc
from abc import abstractmethod


class AbstractRepositoryReadAllAction(abc.ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_all_paginated(self, offset=None, limit=None):
        raise NotImplementedError
