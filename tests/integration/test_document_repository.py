from datetime import datetime

import pytest

from src.adapters.orm import create_tables
from src.adapters.repositories.postgresql import DocumentRepository
from src.domain.entities import Document as DocumentEntity


@pytest.mark.asyncio
async def test_department_repository_create_and_get_all(
        postgres_uri,
        postgres_session_factory,
):
    await create_tables(postgres_uri)
    repo = DocumentRepository(async_session_factory_=postgres_session_factory)

    # add data
    items = [
        DocumentEntity(
            id=1,
            text='Some text 1',
            created_date=datetime.now(),
            rubrics=['RUBRIC-1', 'RUBRIC-2']
        ),
        DocumentEntity(
            id=2,
            text='Some text 2',
            created_date=datetime.now(),
            rubrics=['RUBRIC-1', 'RUBRIC-3']
        )
    ]
    for item in items:
        await repo.create(item)

    # get data
    data = await repo.get_all()
    assert data == items


@pytest.mark.asyncio
async def test_department_repository_create_and_get_all_and_delete(
        postgres_uri,
        postgres_session_factory,
):
    await create_tables(postgres_uri)
    repo = DocumentRepository(async_session_factory_=postgres_session_factory)

    # add data
    items = [
        DocumentEntity(
            id=1,
            text='Some text 1',
            created_date=datetime.now(),
            rubrics=['RUBRIC-1', 'RUBRIC-2']
        ),
        DocumentEntity(
            id=2,
            text='Some text 2',
            created_date=datetime.now(),
            rubrics=['RUBRIC-1', 'RUBRIC-3']
        )
    ]
    for item in items:
        await repo.create(item)

    # get data
    data = await repo.get_all()
    assert data == items

    # delete second record
    await repo.delete_by_id(2)

    # check updates
    data = await repo.get_all()
    assert data == [items[0]]
