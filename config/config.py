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
