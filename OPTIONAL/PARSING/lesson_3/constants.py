import os
import re
from collections import namedtuple
from dotenv import load_dotenv

load_dotenv()

MONGODB_HOST = os.environ.get('MONGODB_HOST')
MONGODB_PORT = int(os.environ.get('MONGODB_PORT'))
MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME')

RE_SALARY = re.compile(r'(?:\d+\s*){1,}')
RE_CURRENCY = re.compile(r'\D+')

MAIN_URL = 'https://hh.ru'
VACANCY_URL = f'{MAIN_URL}/search/vacancy'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}
PARAMS = {
    'text': 'python',  # vacancy_name
    'hhtmFrom': 'vacancy_search_list',
}

Salary = namedtuple('Salary', (
    'min',
    'max',
    'currency'
))
