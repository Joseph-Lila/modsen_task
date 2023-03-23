import os
import tempfile

import pytest
from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src import config


@pytest.fixture
def test_index_title():
    return 'test_index'


@pytest.fixture
def test_index_mappings():
    return {
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


@pytest.fixture
def elasticsearch_host():
    return config.get_test_elasticsearch_uri()


@pytest.fixture
def initial_csv_path():
    return config.get_csv_path_for_testing()


@pytest.fixture
def elastic_client(
        elasticsearch_host,
):
    elastic_client = AsyncElasticsearch(elasticsearch_host)
    return elastic_client


@pytest.fixture
def postgres_uri():
    return config.get_test_postgres_uri()


@pytest.fixture
def postgres_db(
        postgres_uri,
):
    engine = create_async_engine(postgres_uri)
    return engine


@pytest.fixture
def postgres_session_factory(
        postgres_db,
):
    yield sessionmaker(
        bind=postgres_db,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest.fixture
def postgres_session(postgres_session_factory):
    return postgres_session_factory()


@pytest.fixture
def csv_file_path():
    temp = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
    yield temp.name
    temp.close()
    os.unlink(temp.name)
