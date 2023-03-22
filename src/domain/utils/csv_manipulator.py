""" Module srс.domain.utils """

import csv
from dataclasses import asdict
from typing import List

import aiofiles as aiofiles
from aiocsv import AsyncDictReader, AsyncDictWriter
from dateutil.parser import parse
from loguru import logger

from src.domain.entities import Document


class CSVManipulator:
    @staticmethod
    async def read_csv(path: str) -> List[Document]:
        """
        Read and form Document entities from inner csv-data.

        :param path: Str: path to csv-file
        :return: List[Document]
        """

        docs_collection = []
        async with aiofiles.open(
                path,
                mode='r',
                encoding='utf-8',
                newline='',
        ) as afp:
            async for row in AsyncDictReader(afp):
                try:
                    docs_collection.append(
                        Document(
                            id=-1,
                            text=row['text'],
                            created_date=parse(row['created_date']),
                            rubrics=eval(row['rubrics']),
                        )
                    )
                except Exception as e:
                    logger.exception(e)
                    logger.warning(f"Error while converting csv row to object...\nRow: {row}")
        return docs_collection

    @staticmethod
    async def write_csv(path: str, data: List[Document]):
        """
        Write data to csv-file.

        :param path: Str: path to csv-file
        :param data: List[Document]
        :return: None
        """
        async with aiofiles.open(
                path,
                mode='w',
                encoding='utf-8',
                newline='',
        ) as afp:
            writer = AsyncDictWriter(
                afp,
                ["text", "created_date", "rubrics"],
                restval="NULL",
                quoting=csv.QUOTE_ALL,
            )
            await writer.writeheader()
            dataset = []
            for document in data:
                data = asdict(document)
                data.pop('id')
                dataset.append(data)
            await writer.writerows(dataset)
