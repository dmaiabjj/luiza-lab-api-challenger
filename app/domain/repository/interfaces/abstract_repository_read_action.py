import abc
from abc import abstractmethod


class AbstractRepositoryReadAction(abc.ABC):
    @abstractmethod
    def find_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_all_paginated(self, offset=None, limit=None):
        raise NotImplementedError
