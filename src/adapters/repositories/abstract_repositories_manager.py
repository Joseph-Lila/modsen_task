""" Module srс.adapters.repositories """

import abc

from .abstract_repository import AbstractRepository


class AbstractRepositoriesManager(abc.ABC):
    documents: AbstractRepository
