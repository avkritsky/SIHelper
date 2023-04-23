from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import User

class DBRepo:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session


    def add_user(self, new_user: User):
        self.session.add(new_user)

    async def del_user(self, user: str):
        await self.session.execute(
            delete(User).where(
                User.user_id == user
            )
        )

    async def get_user(self, user: User) -> User | None:
        data = await self.session.execute(
            select(User).where(
                User.user_id == user.user_id
            )
        )

        return data.first()

    async def list(self, list_object):
        data = await self.session.execute(
            select(list_object)
        )

        # for row_item in data:
        #     item = row_item

        res = []
        while (item := data.fetchone()) is not None:
            res.append(item[0].output)

        # data = data.fetchmany()
        # print(data)
        #
        # data = [item._asdict() for item in data]

        return res
