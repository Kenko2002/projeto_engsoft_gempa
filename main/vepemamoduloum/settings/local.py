from .base import *
from decouple import config
from os import environ

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-&we(0t(&@t(90rx$19tr3dms-3_4ngz6*6d=9=5ghz=ov#%^4^")
DEBUG = os.environ.get("DEBUG", True) # Padrão True



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
            'ENGINE': config('DB_ENGINE_PRODUCTION', default='django.db.backends.postgresql'),
            "NAME": config("DB_NAME_LOCAL", ""),
            "USER": config("DB_USER_LOCAL", ""),
            "PASSWORD": config("DB_PASSWORD_LOCAL", ""),
            "HOST": config("DB_HOST_LOCAL", ""),
            "PORT": config("DB_PORT_LOCAL", ""),
        },
    }
