from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)

from config import config

engine = create_async_engine(
        url=config.DB_URL,
        isolation_level='REPEATABLE READ'
    )

DEFAULT_SESSION = async_sessionmaker(
    bind=engine
)

async def get_session() -> AsyncSession:
    try:
        db = DEFAULT_SESSION()
        return db
    except Exception as e:
        raise e