from abc import ABC

from app.domain.repository.interfaces.abstract_repository import AbstractRepository
from app.domain.repository.interfaces.abstract_repository_create_action import AbstractRepositoryCreateAction
from app.domain.repository.interfaces.abstract_repository_delete_action import AbstractRepositoryDeleteAction
from app.domain.repository.interfaces.abstract_repository_read_action import AbstractRepositoryReadAction
from app.domain.repository.interfaces.abstract_repository_read_all_action import  \
    AbstractRepositoryReadAllAction
from app.domain.repository.interfaces.abstract_repository_update_action import AbstractRepositoryUpdateAction


class AbstractRepositoryCRUDAction(AbstractRepository, AbstractRepositoryCreateAction, AbstractRepositoryReadAction,
                                   AbstractRepositoryReadAllAction, AbstractRepositoryUpdateAction,
                                   AbstractRepositoryDeleteAction, ABC):
    pass
