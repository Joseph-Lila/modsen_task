import asyncio
import pytest

from src.adapters.orm import create_tables
from src.adapters.repositories.postgresql.repositories_manager import RepositoriesManager
from src.bootstrap import bootstrap
from src.domain.commands import GetFirst20RecordsByMatch, DeleteRecord
from src.domain.events import GotFirst20RecordsByMatch
from src.service_layer.handlers import remove_doc_by_id
from src.service_layer.messagebus import MessageBus


@pytest.mark.asyncio
async def test_get_first_20_records_by_match_sorted(
        postgres_uri,
        postgres_session_factory,
        elastic_client,
        test_index_title,
        initial_csv_path,
):
    manager = RepositoriesManager(async_session_factory_=postgres_session_factory)

    bus: MessageBus = await bootstrap(
        drop_create_tables=True,
        drop_create_index=True,
        init_with_csv=True,
        init_elastic_with_db=True,
        repositories_manager=manager,
        elastic_client=elastic_client,
        index_title=test_index_title,
        initial_csv_path=initial_csv_path,
        connection_string=postgres_uri,
    )

    await asyncio.sleep(2)

    res: GotFirst20RecordsByMatch = await bus.handle_command(
        GetFirst20RecordsByMatch(
            text='Text'
        )
    )

    assert len(res.documents) == 20


@pytest.mark.asyncio
async def test_get_first_20_records_by_match_sorted(
        postgres_uri,
        postgres_session_factory,
        elastic_client,
        test_index_title,
        initial_csv_path,

):
    manager = RepositoriesManager(async_session_factory_=postgres_session_factory)

    bus: MessageBus = await bootstrap(
        drop_create_tables=True,
        drop_create_index=True,
        init_with_csv=True,
        init_elastic_with_db=True,
        repositories_manager=manager,
        elastic_client=elastic_client,
        index_title=test_index_title,
        initial_csv_path=initial_csv_path,
        connection_string=postgres_uri,
    )

    await asyncio.sleep(2)

    # Now there are 21 records
    # Let's delete 2 of them

    await bus.handle_command(DeleteRecord(id_=1))
    await bus.handle_command(DeleteRecord(id_=2))

    await asyncio.sleep(2)

    # (21 - 2) = 19 records
    res: GotFirst20RecordsByMatch = await bus.handle_command(
        GetFirst20RecordsByMatch(
            text='Text'
        )
    )

    assert len(res.documents) == 19
