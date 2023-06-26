pip install --upgrade pip >/dev/null 2>&1
pip install --no-cache-dir --root-user-action=ignore aiogram
pip install --no-cache-dir --root-user-action=ignore httpx
pip install --no-cache-dir --root-user-action=ignore sqlalchemy
pip install --no-cache-dir --root-user-action=ignore redis
pip install --no-cache-dir --root-user-action=ignore pydantic

cd /var/www/html
python src/entrypoints/bot.py