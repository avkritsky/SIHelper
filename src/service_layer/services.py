import json
from typing import Dict
from decimal import Decimal

from src.domain import models
from src.service_layer import unit_of_work
from src.adapters import repository
from config import config


async def load_currency_to_redis(
        redis_uow: unit_of_work.RedisUow = unit_of_work.RedisUow(),
        http_repo: repository.HTTPRepo = repository.HTTPRepo(),
):
    """Get currencies data from API and write to redis"""
    print('Проверка необходимости обновления данных')
    if not await need_update(redis_uow):
        print('Обновление не требуется')
        return
    print('получение данных из API')
    data = await get_currencies_data(http_repo)
    print('запись данных в редис')
    await write_data_to_redis(data, redis_uow)
    print('конец обновления данных')


async def need_update(redis_uow: unit_of_work.RedisUow):
    async with redis_uow:
        data = await redis_uow.repo.get('BTC')

        if data is None:
            return True

        ttl = await redis_uow.repo.ttl('BTC')

        if ttl < config.TTL_FOR_CURR_DATA - 35 * 60:
            return True
    return False


async def write_data_to_redis(data: dict, redis_uow: unit_of_work.RedisUow):
    async with redis_uow as r:
        for key, val in data.items():
            await r.repo.set(
                key,
                val,
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


async def calculate_user_statistic(
        user_transactions: list[models.Transaction],
        currencies_data: dict
):
    """Calculate user statistic. Now, convert to RUB only for mvp"""
    statistic = {}

    if not user_transactions:
        return statistic

    old_costs = Decimal(0)
    new_costs = Decimal(0)

    rub = Decimal(currencies_data.get('RUB', {}).get('price', 0))

    for transaction in user_transactions:
        currency = statistic.setdefault(transaction.target_currency, {})
        currency.setdefault('old', Decimal(0))
        currency.setdefault('new', Decimal(0))
        currency.setdefault('amount', Decimal(0))

        if transaction.from_currency == 'RUB':
            old_cost = Decimal(transaction.from_value)
        elif transaction.from_currency == 'USD':
            old_cost = Decimal(transaction.from_value) * rub
        else:
            curr = transaction.from_currency
            curr_price = Decimal(currencies_data.get(curr, {}).get('price', 0))
            old_cost = Decimal(transaction.from_value) * curr_price * rub

        old_costs += old_cost
        currency['old'] += old_cost

        curr = transaction.target_currency
        curr_price = Decimal(currencies_data.get(curr, {}).get('price', 0))
        new_cost = Decimal(transaction.target_value) * curr_price * rub

        new_costs += new_cost
        currency['new'] += new_cost
        currency['price_$'] = curr_price
        currency['amount'] += Decimal(transaction.target_value)


    for currency, item in statistic.items():
        item[f'{currency}_main_%'] = (item['new']/item['old'])*100


    statistic['all_main_%'] = (new_costs/old_costs) * 100
    statistic['all_main_RUB'] = new_costs - old_costs
    statistic['all_input_RUB'] = old_costs
    statistic['all_output_RUB'] = new_costs

    return statistic



