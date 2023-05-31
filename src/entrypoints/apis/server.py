import asyncio
import os
from typing import Annotated
from asyncio import Lock
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Header, BackgroundTasks, Response
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import CreateTable

from src.service_layer.unit_of_work import get_session, get_redis_uow
from src.entrypoints.apis.routers import (
    root_router,
    transactions_router,
    statistic_router,
)
from src.service_layer import services
from src.domain import models
from config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
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


app = FastAPI(
    title='SIHe 3',
    description='PET PROJECT by AVKRITSKY',
    version='0.1.2023.05.31',
    lifespan=lifespan,
)

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


@app.get('/update_redis_data')
async def update_redis_data():
    try:
        await services.load_currency_to_redis()
    except Exception as e:
        return Response(status_code=503, content=str(e))
    return Response(status_code=200)


app.include_router(root_router.router)
app.include_router(transactions_router.router)
app.include_router(statistic_router.router)
