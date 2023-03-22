""" Module srс.adapters.repositories """

import abc
from typing import List

from src.domain.entities.base_entity import BaseEntity


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def get_all(self) -> List[BaseEntity]:
        """
        Method for getting collection of entities.

        :return: List[BaseEntity]: collection itself
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, id_: int):
        """
        Method for getting entity by the primary key value.

        :param id_: Integer: primary key value
        :return: Optional[BaseEntity]: entity or None-value
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, item: BaseEntity):
        """
        Method for entity creation.

        :param item: BaseEntity
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_by_id(self, id_):
        """
        Method for deleting entity by the primary key value.

        :param id_: Integer: primary key value
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, item):
        """
        Method for updating entity.

        :param item: BaseEntity: future state of entity.
        :return: None
        """
        raise NotImplementedError
