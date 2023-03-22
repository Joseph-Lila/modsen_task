import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, id_):
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_by_id(self, id_):
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, item):
        raise NotImplementedError
