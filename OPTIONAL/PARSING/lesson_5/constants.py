import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_HOST = os.environ.get('MONGODB_HOST')
MONGODB_PORT = int(os.environ.get('MONGODB_PORT'))
MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME')

MONGO_INITDB_ROOT_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')

MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION')

EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

MAIN_URL = os.environ.get('MAIN_URL', 'https://account.mail.ru/login')
