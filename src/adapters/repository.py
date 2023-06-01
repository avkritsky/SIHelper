import asyncio
import json
import pprint
import pickle
from typing import Any

import httpx
import redis.asyncio as redis
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import User, Base, Transaction


class DBRepo:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session


    async def __aenter__(self):
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


    def add(self, item: Base):
        self.session.add(item)


    def add_user(self, new_user: User):
        self.session.add(new_user)

    async def del_user(self, tg_id: str):
        await self.session.execute(
            delete(User).where(
                User.tg_id == tg_id
            )
        )

    async def get_user(self, tg_id: str) -> User | None:
        data = await self.session.execute(
            select(User).where(
                User.tg_id == tg_id
            )
        )

        user = data.scalars().first()

        if user is None:
            return

        await self.session.refresh(user, attribute_names=[
            'transactions',
            'settings',
        ])

        return user

    async def list(self, list_object):
        data = await self.session.execute(
            select(list_object)
        )

        res = []
        while (item := data.fetchone()) is not None:
            res.append(item[0].output)

        return res

    async def del_transaction(self, trans_id: str):
        await self.session.execute(
            delete(Transaction).where(
                Transaction.id == int(trans_id)
            )
        )


class HTTPRepo:

    def __init__(self):
        self.client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        self.client = await httpx.AsyncClient().__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.client.__aexit__(*args)

    async def get(self, url: str) -> tuple[int, str | dict]:
        """Вернёт status code и python-объект ответа"""
        r: httpx.Response = await self.client.get(url)
        return r.status_code, r.json()

    async def post(
            self,
            url: str,
            data: dict | None = None
    ) -> tuple[int, str | dict]:
        r: httpx.Response = await self.client.post(
            url,
            content=json.dumps(data)
        )
        return r.status_code, r.json()


class RedisRepo:
    connect: redis.Redis = None

    def __init__(self, connect: redis.Redis):
        self.connect: redis.Redis = connect

    async def get(self, key: str) -> Any:
        item = await self.connect.get(key)
        if item is None:
            return
        return pickle.loads(item)

    async def list(self) -> dict[str, Any]:
        keys = await self.connect.keys('*')
        data = {}
        for key in keys:
            if isinstance(key, bytes):
                key = key.decode()
            data[key] = await self.get(key)
        return data

    async def set(self, key: str, item: Any, ttl_sec: int | None = None):
        await self.connect.set(
            name=key,
            value=pickle.dumps(item),
            ex=ttl_sec
        )

    async def ttl(self, key: str) -> int:
        ttl = await self.connect.ttl(key)
        return ttl

    async def delete(self, key: str) -> None:
        await self.connect.delete(key)


async def main(repo: HTTPRepo):
    repo = RedisRepo(await redis.Redis())  # "redis://localhost",  db=1))
    #
    for i in range(5):
        await repo.set(f'rest:{i}', {'test': '[p]'}, 60)
    #
    # await asyncio.sleep(1)
    #
    print(await repo.list())
    # print(await repo.ttl('rest'))
    #
    # await repo.delete('rest')
    # print(await repo.get('rest'))
    #
    await repo.connect.close()

    # import os
    # key = os.environ.get('CURRENCY_API_KEY')
    # key2 = os.environ.get('CRYPTO_API_KEY')
    #
    # print(key, type(key))
    # url = ("https://"
    #        "api.freecurrencyapi.com/v1/latest"
    #        "?apikey=")
    # url += key
    # url += '&currencies=EUR%2CAUD%2CRUB'

    #http://api.freecurrencyapi.com/v1/latest?apikey=&currencies=AUD%2CEUR%2CRUB

    #
    # url2 = ("https://pro-api.coinmarketcap.com"
    #         "/v1/cryptocurrency/listings/latest"
    #         "?cryptocurrency_type=all"
    #         "&convert=USD"
    #         f"&CMC_PRO_API_KEY={key2}")

    # print(url)
    # print(url2)
    #
    # async with repo as r:
    #     code, data = await r.get(url)
    #
    # pprint.pprint(data)

    #
    # response = data.get('Valute')
    #
    # pprint.pprint(response)

    # крепта
    # {'data': [{
    #            'id': 1,
    #            'name': 'Bitcoin',
    #            'quote': {'USD': {...,
    #                              'percent_change_1h': -0.19834131,
    #                              'percent_change_24h': -0.78692443,
    #                              'percent_change_30d': -0.75442019,
    #                              'percent_change_60d': 38.11299406,
    #                              'percent_change_7d': -1.01696486,
    #                              'percent_change_90d': 19.77018294,
    #                              'price': 27696.612953640695,
    #                              ...}},
    #            'symbol': 'BTC',},



if __name__ == '__main__':
    asyncio.run(main(HTTPRepo()))
