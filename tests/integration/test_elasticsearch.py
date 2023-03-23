import asyncio

import pytest

from src.adapters.elasticsearch import (add_record, create_index, delete_index,
                                        delete_record,
                                        get_first_20_records_by_match)
from src.domain.commands import (AddRecord, DeleteRecord,
                                 GetFirst20RecordsByMatch)


@pytest.mark.asyncio
async def test_elasticsearch_delete_create_index(
        elastic_client,
        test_index_title,
        test_index_mappings,
):
    # if the index already exists
    try:
        await delete_index(
            elasticsearch_client=elastic_client,
            index_title=test_index_title,
        )
    except Exception as e:
        pass

    # let's create index
    await create_index(
        elasticsearch_client=elastic_client,
        index_title=test_index_title,
        mappings=test_index_mappings,
    )

    # let's delete index
    await delete_index(
        elasticsearch_client=elastic_client,
        index_title=test_index_title,
    )


@pytest.mark.asyncio
async def test_elasticsearch_add_record_and_get_first_20_records_by_match(
        elastic_client,
        test_index_title,
        test_index_mappings,
):
    # if the index already exists
    try:
        await delete_index(
            elasticsearch_client=elastic_client,
            index_title=test_index_title,
        )
    except Exception as e:
        pass

    # let's create index
    await create_index(
        elasticsearch_client=elastic_client,
        index_title=test_index_title,
        mappings=test_index_mappings,
    )

    # prepare data for adding
    items = [
        AddRecord(id_=1, text='Text 1'),
        AddRecord(id_=2, text='Text 2'),
        AddRecord(id_=3, text='Text 3'),
        AddRecord(id_=4, text='Text 4'),
    ]

    # add data
    for item in items:
        await add_record(item, elastic_client, test_index_title)

    # elastic needs time to process my docs
    await asyncio.sleep(2)

    # get results
    result = await get_first_20_records_by_match(
        cmd=GetFirst20RecordsByMatch('Text'),
        elasticsearch_client=elastic_client,
        index_title=test_index_title,
    )

    assert len(result['hits']['hits']) == len(items)

    # let's delete index
    await delete_index(
        elasticsearch_client=elastic_client,
        index_title=test_index_title,
    )


@pytest.mark.asyncio
async def test_elasticsearch_delete_record(
        elastic_client,
        test_index_title,
        test_index_mappings,
):
    # if the index already exists
    try:
        await delete_index(
            elasticsearch_client=elastic_client,
            index_title=test_index_title,
        )
    except Exception as e:
        pass

    # let's create index
    await create_index(
        elasticsearch_client=elastic_client,
        index_title=test_index_title,
        mappings=test_index_mappings,
    )

    # prepare data for adding
    items = [
        AddRecord(id_=1, text='Text 1'),
        AddRecord(id_=2, text='Text 2'),
        AddRecord(id_=3, text='Text 3'),
        AddRecord(id_=4, text='Text 4'),
    ]

    # add data
    for item in items:
        await add_record(item, elastic_client, test_index_title)

    # elastic needs time to process my docs
    await asyncio.sleep(2)

    result = await get_first_20_records_by_match(
        cmd=GetFirst20RecordsByMatch('Text'),
        elasticsearch_client=elastic_client,
        index_title=test_index_title,
    )

    assert len(result['hits']['hits']) == len(items)

    # let's remove record with id=3
    await delete_record(
        cmd=DeleteRecord(id_=3),
        elasticsearch_client=elastic_client,
        index_title=test_index_title,
    )

    # elastic needs time to process my docs
    await asyncio.sleep(2)

    result = await get_first_20_records_by_match(
        cmd=GetFirst20RecordsByMatch('Text'),
        elasticsearch_client=elastic_client,
        index_title=test_index_title,
    )

    assert len(result['hits']['hits']) == len(items) - 1

    # let's delete index
    await delete_index(
        elasticsearch_client=elastic_client,
        index_title=test_index_title,
    )