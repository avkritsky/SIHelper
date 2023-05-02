import asyncio
import json
import pprint

import httpx
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


async def main():

    url = 'https://www.cbr-xml-daily.ru/daily_json.js'

    async with HTTPRepo() as a:
        code, data = await a.get(url)

    print(code)

    pprint.pprint(data)

    # {'Date': '2023-05-03T11:30:00+03:00',
    #  'PreviousDate': '2023-04-29T11:30:00+03:00',
    #  'PreviousURL': '//www.cbr-xml-daily.ru/archive/2023/04/29/daily_json.js',
    #  'Timestamp': '2023-05-02T20:00:00+03:00',
    #  'Valute': {'AED': {'CharCode': 'AED',
    #                     'ID': 'R01230',
    #                     'Name': 'Дирхам ОАЭ',
    #                     'Nominal': 1,
    #                     'NumCode': '784',
    #                     'Previous': 21.9246,
    #                     'Value': 21.7747},
    # 'AMD': {'CharCode': 'AMD',
    #         'ID': 'R01060',
    #         'Name': 'Армянских драмов',
    #         'Nominal': 100,
    #         'NumCode': '051',
    #         'Previous': 20.8228,
    #         'Value': 20.6697},
    # 'AUD': {'CharCode': 'AUD',
    #         'ID': 'R01010',
    #         'Name': 'Австралийский доллар',
    #         'Nominal': 1,
    #         'NumCode': '036',
    #         'Previous': 53.2166,
    #         'Value': 53.6138},
    # 'AZN': {'CharCode': 'AZN',
    #         'ID': 'R01020A',
    #         'Name': 'Азербайджанский манат',
    #         'Nominal': 1,
    #         'NumCode': '944',
    #         'Previous': 47.3584,
    #         'Value': 47.0358},}}


if __name__ == '__main__':
    asyncio.run(main())
