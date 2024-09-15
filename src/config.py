import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    raise Exception('Отстутствует env-файл с переменными окружения')

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not all([DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER, BOT_TOKEN]):
    raise Exception('Отсутствуют необходимые переменные окружения')