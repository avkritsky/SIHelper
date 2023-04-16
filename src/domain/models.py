import pydantic


@pydantic.dataclasses.dataclass
class User:
    user_id: str
    chat_id: str
    fullname: str
    id: int | None = None
