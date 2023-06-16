import os

TELEBOT_TOKEN = os.getenv('TELEBOT_TOKEN')
EXCHANGE_API = os.getenv('EXCHANGE_API')
_DB_LOGIN = os.getenv('DB_LOGIN')
_DB_PASSWORD = os.getenv('DB_PASSWORD')
_DB_HOST = os.getenv('DB_HOST', default='localhost')
_DB_PORT = os.getenv('DB_PORT', default='5432')
_DB_NAME = os.getenv('DB_NAME', default='py40')

DB_URL = f"postgresql+psycopg2://{_DB_LOGIN}:{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}"
