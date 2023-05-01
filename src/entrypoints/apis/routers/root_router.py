import json
from typing import Annotated

from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import models
from src.adapters import repository
from src.service_layer.unit_of_work import get_session

router = APIRouter(
    prefix='/user',
    responses={404: {'data': 'Not found'}}
)


@router.post('/')
async def add_user(
        user: models.ValidateUser,
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ]
) -> Response:
    """Create new user in DB"""
    async with repository.DBRepo(session=session) as repo:
        repo.add(models.User(**user.__dict__))
        await repo.session.commit()

    return Response(
        status_code=200,
        media_type='application/json',
        content=json.dumps(
        {'data': f'Add user {user.fullname}'})
    )


@router.delete('/')
async def del_user(
        tg_id: str,
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ]
) -> Response:
    """Delete user in DB"""
    async with repository.DBRepo(session=session) as repo:
        await repo.del_user(tg_id)
        await repo.session.commit()

    return Response(
        status_code=200,
        media_type='application/json',
        content=json.dumps(
        {'data': f'Del user #{tg_id}'})
    )


@router.get('/')
async def get_user(
        tg_id: str,
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ],
) -> Response:
    """Delete user in DB"""
    async with repository.DBRepo(session=session) as repo:
        user = await repo.get_user(tg_id)

    return Response(
        status_code=200,
        media_type='application/json',
        content=json.dumps(
        {'data': user.output})
    )


@router.get('/all')
async def get_users(
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
        media_type='application/json',
        content=json.dumps(
        {'data': data})
    )
