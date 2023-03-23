""" Module srс """
import asyncio
import inspect

from src.adapters.elasticsearch import (create_index, delete_index,
                                        init_elasticsearch_with_db)
from src.adapters.orm import create_tables
from src.adapters.repositories import AbstractRepositoriesManager
from src.adapters.repositories.postgresql.repositories_manager import (
    RepositoriesManager, init_tables_with_csv)


async def bootstrap(
        drop_create_tables: bool = False,
        drop_create_index: bool = False,
        init_with_csv: bool = False,
        init_elastic_with_db: bool = False,
        repositories_manager: AbstractRepositoriesManager = RepositoriesManager(),
):

    if drop_create_tables:
        await create_tables()

    if drop_create_index:
        try:
            await delete_index()
        except Exception as e:
            pass
        try:
            await create_index()
        except Exception as e:
            pass

    if init_with_csv:
        await init_tables_with_csv(repositories_manager=repositories_manager)

    if init_elastic_with_db:
        await init_elasticsearch_with_db(repositories_manager=repositories_manager)


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)


if __name__ == '__main__':
    asyncio.run(bootstrap())
