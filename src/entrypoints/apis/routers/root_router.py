import json
from typing import Annotated, Coroutine

from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.domain import models
from src.adapters import repository
from src.service_layer.unit_of_work import get_session

router = APIRouter(
    prefix='',
    responses={404: {'data': 'Not found'}}
)


@router.post('/user')
async def add_user(
        user: models.ValidateUser,
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ]
) -> Response:
    """Create new user in DB"""
    async with repository.DBRepo(session=session) as repo:
        repo.add_user(models.User(**user.__dict__))
        await repo.session.commit()

    return Response(
        status_code=200,
        content=json.dumps(
        {'data': f'Add user {user.fullname}'})
    )


@router.delete('/user')
async def dek_user(
        user: str,
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ]
) -> Response:
    """Delete user in DB"""
    async with repository.DBRepo(session=session) as repo:
        await repo.del_user(user)
        await repo.session.commit()

    return Response(
        status_code=200,
        content=json.dumps(
        {'data': f'Del user #{user}'})
    )


@router.get('/users')
async def get_user(
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ],
) -> Response:
    """Delete user in DB"""
    async with repository.DBRepo(session=session) as repo:
        data = await repo.list(models.User)

    return Response(
        status_code=200,
        content=json.dumps(
        {'data': data})
    )
