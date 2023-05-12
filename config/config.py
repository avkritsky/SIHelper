import os

host = 'localhost'
port = 5432
user = os.environ.get('POSTGRES_USER')
user = user.replace('\r', '') if user is not None else None
password = os.environ.get('POSTGRES_PASSWORD')
password = password.replace('\r', '') if password is not None else None
db_name = os.environ.get('POSTGRES_DB')
db_name = db_name.replace('\r', '') if db_name is not None else None

DB_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"

url_currency = ("https://api.freecurrencyapi.com/v1/latest"
                "?apikey={}&currencies=EUR%2CAUD%2CRUB")
url_crypto = ("https://pro-api.coinmarketcap.com"
              "/v1/cryptocurrency/listings/latest"
              "?cryptocurrency_type=all"
              "&convert=USD"
              "&CMC_PRO_API_KEY={}")

CURRENCY_API_KEY = os.environ.get('CURRENCY_API_KEY')
CRYPTO_API_KEY = os.environ.get('CRYPTO_API_KEY')

TTL_FOR_CURR_DATA = 2 * 60 * 60
