from .base import *
from decouple import config

DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config("DJANGO_SECRET_KEY") 


EMAIL_HOST = config('EMAIL_HOST', default='smtp.example.com')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='user@example.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='password')


if config("USE_SQLITE", default=True, cast=bool):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": config("DB_ENGINE_LOCAL", ""),
            "NAME": config("DB_NAME_LOCAL", ""),
            "USER": config("DB_USER_LOCAL", ""),
            "PASSWORD": config("DB_PASSWORD_LOCAL", ""),
            "HOST": config("DB_HOST_LOCAL", ""),
            "PORT": config("DB_PORT_LOCAL", ""),
        },
    }
