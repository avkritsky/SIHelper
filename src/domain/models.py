from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Mapped,
    relationship,
    mapped_column,
)
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
    tg_id: Mapped[str] = mapped_column(unique=True)
    chat_id: Mapped[str]
    fullname: Mapped[str]
    settings: Mapped['Settings'] = relationship(init=False)
    transactions: Mapped[List['Transaction']] = relationship(init=False)


class Settings(Base):
    __tablename__ = 'settings'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    auto_statistic: Mapped[bool]

# alembic или пересоздать базу транзакций
class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    target_currency: Mapped[str]
    target_value: Mapped[str]
    from_currency: Mapped[str]
    from_value: Mapped[str]
    timestamp: Mapped[datetime]


all_tables = (
    User,
    Transaction,
    Settings,
)


class ValidateUser(BaseModel):
    tg_id: str
    chat_id: str
    fullname: str


class ValidateTransaction(BaseModel):
    tg_id: str
    target_currency: str
    target_value: str
    from_currency: str
    from_value: str
