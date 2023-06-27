import asyncio
import json
from typing import Annotated

from fastapi import APIRouter, Response, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import models
from src.adapters import repository
from src.service_layer import services, backgroud_tasks, unit_of_work

router = APIRouter(
    prefix='/statistic',
    responses={404: {'data': 'Not found'}}
)

@router.get('/')
async def get_user_stat(
        tg_id: str,
        redis_uow: Annotated[
            unit_of_work.RedisUow,
            Depends(unit_of_work.get_redis_uow)
        ],
        http_repo: Annotated[
            repository.HTTPRepo,
            Depends(repository.HTTPRepo)
        ],
        session: Annotated[
            AsyncSession,
            Depends(unit_of_work.get_session)
        ],
        back_tasks: BackgroundTasks
) -> Response:
    """Delete user in DB"""

    print('запуск фоновой задачи')
    # back_tasks.add_task(
    #     backgroud_tasks.update_currencies_data,
    #     redis_uow,
    #     http_repo
    # )
    await backgroud_tasks.update_currencies_data(
        redis_uow,
        http_repo,
    )


    print('получение данных из бд')
    async with repository.DBRepo(session=session) as repo:
        user = await repo.get_user(tg_id)

    print('получение данных из редиса')
    async with redis_uow:
        while not (currencies_data := await redis_uow.repo.list()):
            print('hehe')
            await asyncio.sleep(1)


    data = await services.calculate_user_statistic(
        user.transactions,
        currencies_data
    )

    return Response(
        status_code=200,
        media_type='application/json',
        content=json.dumps(data, default=str),
    )
