from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped
from sqlalchemy.orm import mapped_column
from pydantic import BaseModel


class Base(MappedAsDataclass, DeclarativeBase):
    @property
    def output(self):
        return {key: val
                for key, val in self.__dict__.items()
                if not key.startswith('_')}


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[str]
    chat_id: Mapped[str]
    fullname: Mapped[str]

# alembic или пересоздать базу транзакций
class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[str]
    target_currency: Mapped[str]
    target_value: Mapped[str]
    from_currency: Mapped[str]
    from_value: Mapped[str]
    timestamp: Mapped[datetime]


all_tables = (
    User,
    Transaction,
)


class ValidateUser(BaseModel):
    user_id: str
    chat_id: str
    fullname: str
