from .base import *

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'drf',
        'USER': 'gb_drf',
        'PASSWORD': 'gb_drf_password',
        'HOST': 'db',
        'PORT': '5432'
    }
}