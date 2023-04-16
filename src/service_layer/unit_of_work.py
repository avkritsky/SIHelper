from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import config

DEFAULT_SESSION = async_sessionmaker(
    bind=create_async_engine(
        url=config.DB_URL,
        isolation_level='REPEATABLE READ'
    )
)
