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


class DefaultRedis:
    _instance = None

    @property
    async def session(self):
        if self.__class__._instance is None:
            try:
                self.__class__._instance = await redis.Redis()
            except Exception as e:
                print(f'Error connect to redis: {e}')
        return self.__class__._instance


class RedisUow:
    def __init__(self, session_maker=DefaultRedis()):
        self.session_maker = session_maker
        self.repo: repository.RedisRepo | None = None

    async def __aenter__(self):
        connect = await self.session_maker.session
        self.repo = repository.RedisRepo(connect)
        return self

    async def __aexit__(self, *args):
        self.repo = None
        # await self.repo.connect.close()


class FakeUoW(RedisUow):
    def __init__(self, repo):
        self.repo = repo

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


def get_redis_uow():
    return RedisUow()

