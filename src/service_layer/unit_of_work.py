import redis.asyncio as redis
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)

from config import config
from src.adapters import repository


def default_session_maker():
    engine = create_async_engine(
            url=config.DB_URL,
            # echo=True,
            isolation_level='REPEATABLE READ'
        )
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False
    )

def get_session() -> AsyncSession:
    session_maker = default_session_maker()
    return session_maker()


async def get_redis():
    return await redis.Redis()


class RedisUow:
    def __init__(self, session_maker=get_redis):
        self.session_maker = session_maker
        self.repo: repository.RedisRepo | None = None

    async def __aenter__(self):
        connect = await self.session_maker()
        self.repo = repository.RedisRepo(connect)
        return self

    async def __aexit__(self, *args):
        await self.repo.connect.close()


def get_redis_uow():
    return RedisUow()

