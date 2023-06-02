import pytest

from src.service_layer import backgroud_tasks, unit_of_work
from src.adapters import repository

from config import config


@pytest.mark.asyncio
async def test_load_redis_data():

    curr = [
        (
            200,
            {
                'data': {
                    'RUB': 100
                }
            }
        ),
        (
            200,
            {
                'data': [
                    {
                        'symbol': 'BTC'
                    }
                ]
            }
        )
    ]

    redis_uow = unit_of_work.FakeUoW(repository.FakeRepo([None]))
    http_repo = repository.FakeRepo(curr)

    await backgroud_tasks.update_currencies_data(redis_uow, http_repo)

    assert (
               'RUB',
               {'price': 100},
               {'ttl_sec': config.TTL_FOR_CURR_DATA}
           ) in redis_uow.repo.items
