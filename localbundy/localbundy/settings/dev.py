from .base import *
import os
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'localbundytest',
        'USER': 'admin',
        'PASSWORD': 'Password@123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

FRONTEND_URL= config("FRONTEND_URL")
FRONTEND_EMAIL_VERIFY_URL= config("FRONTEND_EMAIL_VERIFY_URL")