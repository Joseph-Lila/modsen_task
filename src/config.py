""" Module srс """
import os
import pathlib

from dotenv import load_dotenv

THIS_DIR = pathlib.Path(__file__).parent.resolve().absolute()
ROOT_DIR = THIS_DIR.parent
DOTENV_PATH = ROOT_DIR / '.env'


# load secret data from .env
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)


def get_test_postgres_uri() -> str:
    """
    Method to get connection string for testing PostgreSQL server.
    :return: str: connection string.
    """
    host = os.environ['POSTGRESQL_TEST_HOST']
    port = os.environ['POSTGRESQL_TEST_PORT']
    password = os.environ['POSTGRESQL_TEST_PASSWORD']
    user = os.environ['POSTGRESQL_TEST_USERNAME']
    db_name = os.environ['POSTGRESQL_TEST_MAINTENANCE_DATABASE']
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


def get_postgres_uri() -> str:
    """
    Method to get connection string for PostgreSQL server.
    :return: str: connection string.
    """
    host = os.environ['POSTGRESQL_HOST']
    port = os.environ['POSTGRESQL_PORT']
    password = os.environ['POSTGRESQL_PASSWORD']
    user = os.environ['POSTGRESQL_USERNAME']
    db_name = os.environ['POSTGRESQL_MAINTENANCE_DATABASE']
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


def get_test_data_csv_path() -> str:
    """
    Method to get path to csv file with test data.
    :return: Str: path to csv.
    """
    return str(ROOT_DIR / 'assets' / 'task' / 'posts.csv')


def get_csv_path_for_testing() -> str:
    """
    Method to get path to csv file with data for testing.
    :return: Str: path to csv.
    """
    return str(ROOT_DIR / 'assets' / 'task' / 'test_data.csv')


def get_elasticsearch_uri() -> str:
    """
    Method to get elasticsearch uri.
    :return: str: uri.
    """
    host = os.environ['ELASTICSEARCH_URI']
    return host


def get_test_elasticsearch_uri() -> str:
    """
    Method to get elasticsearch test uri.
    :return: str: uri.
    """
    host = os.environ['ELASTICSEARCH_TEST_URI']
    return host
