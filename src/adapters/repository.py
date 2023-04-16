from sqlalchemy import select
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

    async def get_user(self, user: User) -> User | None:
        data = await self.session.execute(
            select(User).where(
                User.user_id == user.user_id
            )
        )

        return data.first()
