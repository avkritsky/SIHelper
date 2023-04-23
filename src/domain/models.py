from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import registry
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from pydantic import BaseModel

print('MAPPED')

class Base(MappedAsDataclass, DeclarativeBase):
    ...

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[str]
    chat_id: Mapped[str]
    fullname: Mapped[str]

    @property
    def output(self):
        return {key: val
                for key, val in self.__dict__.items()
                if not key.startswith('_')}


class ValidateUser(BaseModel):
    user_id: str
    chat_id: str
    fullname: str


# metadata = MetaData()
#
# users_table = Table(
#     'public.users',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('user_id', String(25)),
#     Column('chat_id', String(25)),
#     Column('fullname', String(255))
# )
#
#
# def start_mapper():
#     reg = registry(metadata=metadata)
#     reg.map_imperatively(models.User, users_table)
    # mapper(models.User, users_table)
