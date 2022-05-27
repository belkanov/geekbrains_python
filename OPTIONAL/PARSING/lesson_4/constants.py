import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_HOST = os.environ.get('MONGODB_HOST')
MONGODB_PORT = int(os.environ.get('MONGODB_PORT'))
MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME')

MONGO_INITDB_ROOT_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')

MONGO_COLLECTION = 'mailru_main_news'

MAIN_URL = 'https://news.mail.ru/'
XPATH_ANCHOR = '//table[@class="daynews__inner"]'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}
PARAMS = {
}
