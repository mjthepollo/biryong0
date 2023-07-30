from config.settings.local import *  # noqa

STATIC_URL = "/staticfiles/"  # TEMP!!!!!!!!!!!
ALLOWED_HOSTS = ["*"]

DEBUG = False
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "https://ddshs.co.kr",
    "http://ddshs.co.kr",
    "http://20.39.198.155",

]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'ddshs',
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'HOST': 'biryong0db.postgres.database.azure.com'
    }
}
