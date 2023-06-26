import logging
from decimal import Decimal

from aiogram import Bot, Dispatcher, executor, types

from src.adapters import repository
from config import config


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.TG_API_KEY)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.\n"
                        f"Your TG_ID: {message.from_user.id}\n"
                        f"Use /stat")


@dp.message_handler(commands=['stat', 'стат'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    async with repository.HTTPRepo() as client:
        code, data = await client.get(
            f'{config.API_USER_STAT_ROUTE}{message.from_user.id}'
        )

    if code == 200:
        response = "Ваша статистика:\n"

        for key, val in data.items():
            if 'all_' in key:
                continue
            response += f'\nСтатистика для {key}:'
            key_profit = round(Decimal(val.get(f'{key}_main_%', '0')), 2)
            response += f"""
            В наличии: {val.get('amount', 0)} {key}
            Текущая цена: {round(Decimal(val.get('price_$', '0')), 2)} $
            Потрачено: {round(Decimal(val.get('old', '0')), 2)} р.
            Потенциальная прибыль: {round(Decimal(val.get('new', '0')), 2)} р.
            П.Прибыль (%): {key_profit}
            """

        all_prc = round(Decimal(data.get(f'all_main_%', '0')), 2)
        all_rub = round(Decimal(data.get(f'all_main_RUB', '0')), 2)
        all_old = round(Decimal(data.get(f'all_input_RUB', '0')), 2)
        all_new = round(Decimal(data.get(f'all_output_RUB', '0')), 2)

        response += f"""\nИтого, общая статистика:
            Общая прибыль: {all_prc} %
            Общая прибыль в рублях: {all_rub} р.
            Всего потрачено: {all_old} р.
            Всего можно вернуть: {all_new} р.
        """

    else:
        response = f"I can't get your stat :("

    await message.reply(response)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
