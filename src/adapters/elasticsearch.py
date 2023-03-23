from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch

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


async def create_index(
        elasticsearch_client: AsyncElasticsearch,
        index_title=INDEX_TITLE,
        mappings=MAPPING_FOR_INDEX,
):
    """
    Method to create an index.

    :param elasticsearch_client: AsyncElasticsearch: client instance
    :param index_title: str
    :param mappings: dict
    :return: None
    """
    await elasticsearch_client.indices.create(
        index=index_title,
        mappings=mappings,
    )


async def delete_index(
        elasticsearch_client: AsyncElasticsearch,
        index_title=INDEX_TITLE,
):
    """
    Method to delete an index.

    :param elasticsearch_client: AsyncElasticsearch: client instance
    :param index_title: str
    :return: None
    """
    await elasticsearch_client.indices.delete(index=index_title)


async def add_record(
        cmd: AddRecord,
        elasticsearch_client: AsyncElasticsearch,
        index_title=INDEX_TITLE,
) -> ObjectApiResponse:
    """
    Method to add a document in the index.

    :param cmd: AddRecord: contains id and text
    :param elasticsearch_client: AsyncElasticsearch: client instance
    :param index_title: str
    :return: ObjectApiResponse
    """
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
        elasticsearch_client: AsyncElasticsearch,
        index_title=INDEX_TITLE,
):
    """
    Method to delete a document in the index.

    :param cmd: DeleteRecord: contains doc_id (from database)
    :param elasticsearch_client: AsyncElasticsearch: client instance
    :param index_title: str
    :return: None
    """
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
        elasticsearch_client: AsyncElasticsearch,
        index_title=INDEX_TITLE,
) -> ObjectApiResponse:
    """
    Method to get first 20 records by text match.

    :param cmd: GetFirst20RecordsByMatch: contains search text
    :param elasticsearch_client: AsyncElasticsearch: client instance
    :param index_title: str
    :return: ObjectApiResponse
    """
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
        elasticsearch_client: AsyncElasticsearch,
        index_title: str,
):
    """
    Method to initialize elasticsearch with data in the database.

    :param repositories_manager: AbstractRepositoriesManager
    :param elasticsearch_client: AsyncElasticsearch
    :param index_title: str
    :return: None
    """
    documents = await repositories_manager.documents.get_all()
    for doc in documents:
        await add_record(
            AddRecord(
                id_=doc.id,
                text=doc.text,
            ),
            elasticsearch_client=elasticsearch_client,
            index_title=index_title,
        )
