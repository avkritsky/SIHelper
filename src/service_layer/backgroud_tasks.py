from src.service_layer import services

async def update_currencies_data():
    print('update redis data')
    try:
        await services.load_currency_to_redis()
    except Exception as e:
        print(f'Error update currencies data: {e}')