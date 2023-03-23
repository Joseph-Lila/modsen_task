from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src import config
from src.domain.utils import CSVManipulator

from ...orm import async_session_factory
from ..abstract_repositories_manager import AbstractRepositoriesManager
from . import DocumentRepository


class RepositoriesManager(AbstractRepositoriesManager):
    def __init__(self, async_session_factory_: async_sessionmaker[AsyncSession] = async_session_factory):
        self.documents = DocumentRepository(async_session_factory_)


async def init_tables_with_csv(
        repositories_manager=RepositoriesManager(),
        csv_path=config.get_test_data_csv_path(),
):
    dataset = await CSVManipulator.read_csv(csv_path)
    for record in dataset:
        await repositories_manager.documents.create(record)
