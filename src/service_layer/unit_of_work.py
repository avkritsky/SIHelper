from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)

from config import config


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