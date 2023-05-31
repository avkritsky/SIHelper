import json
from typing import Annotated

from fastapi import APIRouter, Response, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import models
from src.adapters import repository
from src.service_layer import services, backgroud_tasks
from src.service_layer.unit_of_work import get_session

router = APIRouter(
    prefix='/statistic',
    responses={404: {'data': 'Not found'}}
)

@router.get('/')
async def get_user_stat(
        tg_id: str,
        session: Annotated[
            AsyncSession,
            Depends(get_session)
        ],
        back_tasks: BackgroundTasks
) -> Response:
    """Delete user in DB"""
    back_tasks.add_task(backgroud_tasks.update_currencies_data)
    await services.calculate_user_statistic(tg_id)

    return Response(
        status_code=200,
        media_type='application/json',
        content=None
    )
