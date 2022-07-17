from .common import *

DEBUG = True
SECRET_KEY = 'django-insecure-6j2@8g)ygvsiuvnh1w8cs&o)k**r'

ALLOWED_HOSTS = ["*"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'db',
#         'PORT': 5432
#     }
# }