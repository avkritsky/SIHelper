from src.service_layer import services, unit_of_work
from src.adapters import repository


async def update_currencies_data(
        redis_uow: unit_of_work.RedisUow,
        http_repo: repository.AbstractRepo,
):
    print('update redis data')
    try:
        await services.load_currency_to_redis(redis_uow, http_repo)
    except Exception as e:
        print(f'Error update currencies data: {e}')