import os

host = 'localhost'
port = 5432
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')

DB_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
