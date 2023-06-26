pip install --upgrade pip >/dev/null 2>&1
pip install --no-cache-dir --root-user-action=ignore -r /var/www/html/requirements.txt
cd /var/www/html
uvicorn src.entrypoints.apis.server:app --host 0.0.0.0 --port 8031