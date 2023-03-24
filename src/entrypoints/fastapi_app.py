""" Module srс.entrypoints """
import argparse

import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter
from starlette.requests import Request

from src import config
from src.bootstrap import bootstrap
from src.domain.commands import GetFirst20RecordsByMatch, DeleteRecord
from src.service_layer.messagebus import MessageBus

app = FastAPI()
elastic_client = AsyncElasticsearch(config.get_elasticsearch_uri())


@app.on_event("shutdown")
async def app_shutdown():
    await elastic_client.close()


@app.on_event("startup")
async def startup_event():
    bus = await bootstrap(
        drop_create_tables=app.state.drop_create_tables,
        drop_create_index=app.state.drop_create_indices,
        init_with_csv=app.state.init_with_csv,
        initial_csv_path=app.state.initial_csv_path,
        init_elastic_with_db=app.state.init_elastic_with_db,
    )

    app.state.bus = bus


async def get_20_matches(request: Request, text: str):
    bus: MessageBus = request.app.state.bus
    cmd: GetFirst20RecordsByMatch = GetFirst20RecordsByMatch(text=text)
    result = await bus.handle_command(cmd)
    return {"result": result}


async def remove_by_id(request: Request, id_: int):
    bus: MessageBus = request.app.state.bus
    cmd: DeleteRecord = DeleteRecord(id_=id_)
    result = await bus.handle_command(cmd)
    return {"result": result}


routes = [
    APIRoute(path='/get_20_matches', endpoint=get_20_matches, methods=['GET']),
    APIRoute(path='/remove_by_id', endpoint=remove_by_id, methods=['GET']),
]


def main():
    parser = argparse.ArgumentParser(
        description='Search service made by LLK (Artur Prakapenka)',
    )
    parser.add_argument(
        '--drop_create_tables',
        type=bool,
        default=False,
        help='Do you want to drop and create tables in database?',
    )
    parser.add_argument(
        '--drop_create_indices',
        type=bool,
        default=False,
        help='Do you want to drop and create index in elasticsearch?',
    )
    parser.add_argument(
        '--init_with_csv',
        type=bool,
        default=False,
        help='Do you want to to init database with csv?',
    )
    parser.add_argument(
        '--initial_csv_path',
        type=str,
        default='',
        help='Define path for csv with initial data?',
    )
    parser.add_argument(
        '--init_elastic_with_db',
        type=bool,
        default=False,
        help='Do you want to fill elasticsearch index with documents from database?',
    )
    args = parser.parse_args()

    app.state.drop_create_tables = args.drop_create_tables
    app.state.drop_create_indices = args.drop_create_indices
    app.state.init_with_csv = args.init_with_csv
    app.state.initial_csv_path = args.initial_csv_path
    app.state.init_elastic_with_db = args.init_elastic_with_db

    app.include_router(APIRouter(routes=routes))
    uvicorn.run(app)


if __name__ == '__main__':
    main()
