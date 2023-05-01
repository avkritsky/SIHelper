import json
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import models
from src.adapters import repository
from src.service_layer.unit_of_work import get_session

router = APIRouter(
    prefix='/transaction',
    responses={404: {'data': 'Not found'}}
)


@router.get('/')
async def get_user_transactions(
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
        {'data': [transaction.output for transaction in user.transactions]})
    )


@router.post('/')
async def add_transaction(
        transaction: models.ValidateTransaction,
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ]
) -> Response:
    """Add new transaction record in DB"""
    async with repository.DBRepo(session=session) as repo:
        user = await repo.get_user(transaction.tg_id)

        repo.add(
            models.Transaction(
                user_id=user.id,
                target_currency=transaction.target_currency,
                target_value=transaction.target_value,
                from_currency=transaction.from_currency,
                from_value=transaction.from_value,
                timestamp=datetime.now(),
            )
        )
        await repo.session.commit()

    return Response(
        status_code=200,
        media_type='application/json',
        content=json.dumps(
        {'data': f'Add transaction for user #{transaction.tg_id}'})
    )
