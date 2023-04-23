from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped
from sqlalchemy.orm import mapped_column
from pydantic import BaseModel


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
