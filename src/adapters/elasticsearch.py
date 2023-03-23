from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch

from src import config
from src.adapters.repositories import AbstractRepositoriesManager
from src.domain.commands import (AddRecord, DeleteRecord,
                                 GetFirst20RecordsByMatch)

INDEX_TITLE = 'documents'
MAPPING_FOR_INDEX = {
    'properties': {
        'id': {
            'type': 'long',
        },
        'text': {
            'type': 'text',
            'fields': {
                'raw': {
                    'type': 'keyword',
                }
            }
        }
    }
}


elastic_client = AsyncElasticsearch(config.get_elasticsearch_uri())


async def create_index(
        elasticsearch_client: AsyncElasticsearch = elastic_client,
        index_title=INDEX_TITLE,
        mappings=MAPPING_FOR_INDEX,
):
    await elasticsearch_client.indices.create(
        index=index_title,
        mappings=mappings,
    )


async def delete_index(
        elasticsearch_client: AsyncElasticsearch = elastic_client,
        index_title=INDEX_TITLE,
):
    await elasticsearch_client.indices.delete(index=index_title)


async def add_record(
        cmd: AddRecord,
        elasticsearch_client: AsyncElasticsearch = elastic_client,
        index_title=INDEX_TITLE,
) -> ObjectApiResponse:
    result = await elasticsearch_client.index(
        index=index_title,
        document={
            'id': cmd.id_,
            'text': cmd.text,
        },
    )
    return result


async def delete_record(
        cmd: DeleteRecord,
        elasticsearch_client: AsyncElasticsearch = elastic_client,
        index_title=INDEX_TITLE,
):
    await elasticsearch_client.delete_by_query(
        index=index_title,
        query={
            "match": {
                'id': cmd.id_,
            }
        },
    )


async def get_first_20_records_by_match(
        cmd: GetFirst20RecordsByMatch,
        elasticsearch_client: AsyncElasticsearch = elastic_client,
        index_title=INDEX_TITLE,
) -> ObjectApiResponse:
    result = await elasticsearch_client.search(
        index=index_title,
        size=20,
        query={
            "match": {
                "text": cmd.text,
            },
        },
    )
    return result


async def init_elasticsearch_with_db(
        repositories_manager: AbstractRepositoriesManager,
        elasticsearch_client: AsyncElasticsearch = elastic_client,
):
    documents = await repositories_manager.documents.get_all()
    for doc in documents:
        await add_record(
            AddRecord(
                id_=doc.id,
                text=doc.text,
            ),
            elasticsearch_client=elasticsearch_client,
        )
