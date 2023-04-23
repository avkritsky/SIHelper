from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import User

class DBRepo:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session


    async def __aenter__(self):
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


    def add_user(self, new_user: User):
        self.session.add(new_user)

    async def del_user(self, user_id: str):
        await self.session.execute(
            delete(User).where(
                User.user_id == user_id
            )
        )

    async def get_user(self, user_id: str) -> User | None:
        data = await self.session.execute(
            select(User).where(
                User.user_id == user_id
            )
        )

        data = data.first()

        if data is not None:
            data = data[0].output

        return data

    async def list(self, list_object):
        data = await self.session.execute(
            select(list_object)
        )

        res = []
        while (item := data.fetchone()) is not None:
            res.append(item[0].output)

        return res
