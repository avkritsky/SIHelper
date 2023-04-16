from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import mapper

from src.domain import models


metadata = MetaData()

users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', String(25)),
    Column('chat_id', String(25)),
    Column('fullname', String(255))
)


def start_mapper():
    mapper(models.User, users_table)
