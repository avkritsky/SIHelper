from typing import Annotated

from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.domain import models
from src.adapters import repository
from src.service_layer.unit_of_work import DEFAULT_SESSION

router = APIRouter(
    prefix='',
    responses={404: {'description': 'Not found'}}
)


@router.post('/user')
async def add_user(
        user: models.User,
        session: Annotated[
            async_sessionmaker,
            Depends(DEFAULT_SESSION)
        ]
) -> Response:
    """Create new user in DB"""
    repo = repository.DBRepo(session=session())

    repo.add_user(user)

    return Response(status_code=200,
                    content={'description': f'Add user {user.fullname}'})
