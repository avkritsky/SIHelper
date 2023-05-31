import asyncio
import os
from typing import Annotated
from asyncio import Lock
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import CreateTable

from src.service_layer.unit_of_work import get_session, get_redis_uow
from src.entrypoints.apis.routers import root_router, transactions_router
from src.service_layer import services
from src.domain import models
from config import config


@asynccontextmanager
async def lifespan():
    if config.user is None:
        print('тестовое окружение')
        yield
        return

    session = get_session()

    async with session:
        for table in models.all_tables:
            create_expression = CreateTable(
                table.__table__,
                if_not_exists=True
            )

            await session.execute(create_expression)
            await session.commit()
        yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


locker = Lock()


# @app.get('/')
# async def exe_pep():
#     res = await services.load_currency_to_redis()
#     return res


async def start_load_currencies_data(locker: asyncio.Lock):
    print('update redis data')
    await services.load_currency_to_redis()
    locker.release()



@app.middleware('http')
async def update_redis_data(
        request: Request,
        call_next,
        back_task: BackgroundTasks,
):
    if config.user is None or request.method not in {'GET', 'POST'}:
        print('тестовое окружение')
        return await call_next(request)

    redis = get_redis_uow()

    async with redis as r:
        item = await r.repo.get('BTC')

        if item is None or await r.repo.ttl('BTC') < 300:
            while locker.locked():
                await asyncio.sleep(0.1)
            else:
                await locker.acquire()
                back_task.add_task(start_load_currencies_data, locker)

    return await call_next(request)


app.include_router(root_router.router)
app.include_router(transactions_router.router)
