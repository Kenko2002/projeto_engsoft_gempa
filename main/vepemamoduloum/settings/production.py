from .base import *
from decouple import config
import dj_database_url

DEBUG = False

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE_PRODUCTION', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME_PRODUCTION', default='db.sqlite3'),  # Or path if not in project root
        'USER': config('DB_USER_PRODUCTION', default=''),  # Blank for SQLite
        'PASSWORD': config('DB_PASSWORD_PRODUCTION', default=''), # Blank for SQLite
        'HOST': config('DB_HOST_PRODUCTION', default=''),  # Blank for SQLite
        'PORT': config('DB_PORT_PRODUCTION', default=''),  # Blank for SQLite
    }
}
