from datetime import datetime

import pytest

from src.domain.entities import Document
from src.domain.utils import CSVManipulator


@pytest.mark.asyncio
async def test_csv_manipulator_read_write(
    csv_file_path,
):
    # prepare data
    # ids must be -1 becouse
    items = [
        Document(
            id=-1,
            text='Some text 1',
            created_date=datetime.now(),
            rubrics=['RUBRIC-1', 'RUBRIC-2']
        ),
        Document(
            id=-1,
            text='Some text 2',
            created_date=datetime.now(),
            rubrics=['RUBRIC-1', 'RUBRIC-3']
        )
    ]

    # write data
    await CSVManipulator.write_csv(csv_file_path, items)

    # read data
    data = await CSVManipulator.read_csv(csv_file_path)

    assert data == items
