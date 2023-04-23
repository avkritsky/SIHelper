import os

host = 'localhost'
port = 5432
user = os.environ.get('POSTGRES_USER').replace('\r', '')
password = os.environ.get('POSTGRES_PASSWORD').replace('\r', '')
db_name = os.environ.get('POSTGRES_DB').replace('\r', '')

DB_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
