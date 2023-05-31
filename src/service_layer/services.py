import json
from typing import Dict

from src.service_layer import unit_of_work
from src.adapters import repository
from config import config


async def load_currency_to_redis(
        redis_uow: unit_of_work.RedisUow = unit_of_work.RedisUow(),
        http_repo: repository.HTTPRepo = repository.HTTPRepo(),
):
    """Get currencies data from API and write to redis"""
    data = await get_currencies_data(http_repo)
    await write_data_to_redis(data, redis_uow)


async def write_data_to_redis(data: dict, redis_uow: unit_of_work.RedisUow):
    async with redis_uow as r:
        for key, val in data.items():
            await r.repo.set(
                key,
                json.dumps(val),
                ttl_sec=config.TTL_FOR_CURR_DATA
            )


async def get_currencies_data(
        http_repo: repository.HTTPRepo
) -> Dict[str, dict]:
    async with http_repo as r:
        url = config.url_currency.format(
            config.CURRENCY_API_KEY.replace('\r', '')
        )
        code, data = await r.get(url)

        if code == 200:
            currency_data = load_data(data)
        else:
            currency_data = {}

        url = config.url_crypto.format(config.CRYPTO_API_KEY)
        code, data = await r.get(url)

        if code == 200:
            crypto_data = format_crypto_data(data)
        else:
            crypto_data = {}

    return {**currency_data, **crypto_data}


def load_data(raw_data: dict) -> dict:
    data = raw_data.get('data', {})
    data = {key: {'price': val} for key, val in data.items()}
    return data


def format_crypto_data(raw_data: dict) -> dict:
    data: list[dict] = raw_data.get('data')
    resp = {}

    for item in data:
        symbol = item.get('symbol')
        quote = item.get('quote', {}).get('USD', {})
        resp[symbol] = {
            'name': item.get('name'),
            'price': quote.get('price'),
            'statistic': quote,
        }

    return resp


async def calculate_user_statistic(user_tg_id: str):
    ...
