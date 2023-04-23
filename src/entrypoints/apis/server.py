from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import CreateTable

from src.service_layer.unit_of_work import get_session, engine
from src.entrypoints.apis.routers import root_router
from src.domain import models
from src.service_layer import unit_of_work

app = FastAPI()

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


@app.on_event('startup')
async def on_start():
    session = await get_session()

    async with session:

        create_expression = CreateTable(
            models.User.__table__,
            if_not_exists=True
        )

        await session.execute(create_expression)
        await session.commit()


app.include_router(root_router.router)
