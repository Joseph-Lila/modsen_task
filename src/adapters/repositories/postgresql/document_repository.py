""" Module srс.adapters.repositories.postgresql """

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import immediateload

from src.adapters.orm import (Document, DocumentRubric, Rubric,
                              async_session_factory)
from src.adapters.repositories import AbstractRepository
from src.domain.entities import Document as DocumentEntity


class DocumentRepository(AbstractRepository):
    def __init__(self, async_session_factory_: async_sessionmaker[AsyncSession] = async_session_factory):
        self.async_session: async_sessionmaker[AsyncSession] = async_session_factory_

    async def get_all(self):
        async with self.async_session() as session:
            stmt = select(Document).options(immediateload(Document.rubrics))
            items = await session.scalars(stmt)
        answer = [
            DocumentEntity(
                id=item.id,
                text=item.text,
                rubrics=[rubric.value for rubric in item.rubrics],
                created_date=item.created_date,
            )
            for item in items
        ]
        return answer

    async def get_by_id(self, id_):
        raise NotImplementedError

    async def create(self, item: DocumentEntity):
        async with self.async_session() as session:
            async with session.begin():

                # create rubrics if needed
                rubric_ids = []
                for rubric in item.rubrics:
                    stmt = select(Rubric.id).filter_by(value=rubric)
                    rubric_id = await session.scalar(stmt)
                    if rubric_id is None:
                        new_rubric = Rubric(value=rubric)
                        session.add(new_rubric)
                        await session.flush()
                        rubric_ids.append(new_rubric.id)
                    else:
                        rubric_ids.append(rubric_id)

                logger.info(f"Rubric_ids: {rubric_ids}")

                # create the document
                new_document = Document(text=item.text)
                session.add(new_document)
                await session.flush()

                # create document rubrics
                for rubric_id in rubric_ids:
                    session.add(
                        DocumentRubric(
                            document_id=new_document.id,
                            rubric_id=rubric_id,
                        )
                    )

    async def delete_by_id(self, id_):
        async with self.async_session() as session:
            async with session.begin():
                stmt = delete(DocumentRubric).filter_by(document_id=id_)
                await session.execute(stmt)
                stmt = delete(Document).filter_by(id=id_)
                await session.execute(stmt)

    async def update(self, item):
        raise NotImplementedError
