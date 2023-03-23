""" Module srс.service_layer """
from typing import Callable, Dict, Type

from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch

from src.adapters.elasticsearch import (delete_record,
                                        get_first_20_records_by_match)
from src.adapters.repositories import AbstractRepositoriesManager
from src.domain.commands import DeleteRecord, GetFirst20RecordsByMatch
from src.domain.commands.command import Command
from src.domain.entities import Document
from src.domain.events import DocumentIsDeleted, GotFirst20RecordsByMatch


def sort_by_date(doc: Document):
    return doc.created_date


async def get_first_20_records_by_match_sorted(
        cmd: GetFirst20RecordsByMatch,
        repositories_manager: AbstractRepositoriesManager,
        elastic_client: AsyncElasticsearch,
        index_title: str,
) -> GotFirst20RecordsByMatch:
    result: ObjectApiResponse = await get_first_20_records_by_match(
        cmd=cmd,
        elasticsearch_client=elastic_client,
        index_title=index_title,
    )
    ids = [value['_source']['id'] for value in result['hits']['hits']]
    documents = []
    for id_ in ids:
        doc = await repositories_manager.documents.get_by_id(id_)
        if doc is not None:
            documents.append(doc)
    documents.sort(key=sort_by_date)
    return GotFirst20RecordsByMatch(documents=documents)


async def remove_doc_by_id(
        cmd: DeleteRecord,
        repositories_manager: AbstractRepositoriesManager,
        elastic_client: AsyncElasticsearch,
        index_title: str,
) -> DocumentIsDeleted:
    # remove from elastic
    await delete_record(
        cmd=cmd,
        elasticsearch_client=elastic_client,
        index_title=index_title,
    )

    # delete from database
    await repositories_manager.documents.delete_by_id(cmd.id_)

    return DocumentIsDeleted()


COMMAND_HANDLERS = {
    GetFirst20RecordsByMatch: get_first_20_records_by_match_sorted,
    DeleteRecord: remove_doc_by_id,
}  # type: Dict[Type[Command], Callable]
