import os

from dotenv import load_dotenv


load_dotenv()

TELEBOT_TOKEN = os.getenv('TELEBOT_TOKEN')
EXCHANGE_API = os.getenv('EXCHANGE_API')
LOCALIZATION = os.getenv('LOCALIZATION', default='RUS')
_DB_LOGIN = os.getenv('DB_LOGIN', default='bot_exchange')
_DB_PASSWORD = os.getenv('DB_PASSWORD', default='bot_exchange')
_DB_HOST = os.getenv('DB_HOST', default='127.0.0.1')
_DB_PORT = os.getenv('DB_PORT', default='5432')
_DB_NAME = os.getenv('DB_NAME', default='exchange_db')
DB_URL = f"postgresql://{_DB_LOGIN}:{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}"
