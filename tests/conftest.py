import pytest

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)
from sqlalchemy.schema import CreateTable

from src.domain import models
from src.service_layer.unit_of_work import get_session
from src.entrypoints.apis.server import app


engine = create_async_engine(
        url='sqlite+aiosqlite:///:memory:',
        echo=True
)

DEFAULT_SESSION = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

session = DEFAULT_SESSION()


def session_test():
    return session


@pytest.fixture(scope='function')
def create_db():
    async def wrap(session):
        async with session:

            create_expression = CreateTable(
                models.User.__table__,
                if_not_exists=True
            )

            await session.execute(create_expression)
            await session.commit()
    return wrap


@pytest.fixture(scope='function')
def client_test():
    app.dependency_overrides[get_session] = session_test

    with TestClient(app) as client:
        yield client, session_test()
