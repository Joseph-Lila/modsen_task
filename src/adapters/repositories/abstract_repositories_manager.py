import abc

from .abstract_repository import AbstractRepository


class AbstractRepositoriesManager(abc.ABC):
    documents: AbstractRepository
