""" Module srс """
import inspect

from elasticsearch import AsyncElasticsearch

from src import config
from src.adapters.elasticsearch import (create_index, delete_index,
                                        init_elasticsearch_with_db, INDEX_TITLE, MAPPING_FOR_INDEX)
from src.adapters.orm import create_tables
from src.adapters.repositories import AbstractRepositoriesManager
from src.adapters.repositories.postgresql.repositories_manager import (
    RepositoriesManager, init_tables_with_csv)
from src.service_layer import handlers
from src.service_layer.messagebus import MessageBus


async def bootstrap(
        drop_create_tables: bool = False,
        drop_create_index: bool = False,
        init_with_csv: bool = False,
        initial_csv_path: str = config.get_test_data_csv_path(),
        init_elastic_with_db: bool = False,
        repositories_manager: AbstractRepositoriesManager = RepositoriesManager(),
        elastic_client: AsyncElasticsearch = AsyncElasticsearch(config.get_elasticsearch_uri()),
        index_title: str = INDEX_TITLE,
        mappings: dict = MAPPING_FOR_INDEX,
        connection_string=config.get_postgres_uri()
) -> MessageBus:

    if drop_create_tables:
        await create_tables(connection_string=connection_string)

    if drop_create_index:
        try:
            await delete_index(
                elasticsearch_client=elastic_client,
                index_title=index_title,
            )
        except Exception as e:
            pass
        try:
            await create_index(
                elasticsearch_client=elastic_client,
                index_title=index_title,
                mappings=mappings,
            )
        except Exception as e:
            pass

    if init_with_csv and initial_csv_path:
        await init_tables_with_csv(
            repositories_manager=repositories_manager,
            csv_path=initial_csv_path,
        )

    if init_elastic_with_db:
        await init_elasticsearch_with_db(
            repositories_manager=repositories_manager,
            elasticsearch_client=elastic_client,
            index_title=index_title,
        )

    dependencies = {
        "repositories_manager": repositories_manager,
        "elastic_client": elastic_client,
        "index_title": index_title,
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return MessageBus(
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
