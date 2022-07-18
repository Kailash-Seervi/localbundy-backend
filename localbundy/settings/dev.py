from .base import *
import os
from decouple import config

DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_PASSWORD = config('DB_PASSWORD')
DB_USER = config('DB_USER')
DB_ENGINE = config('DB_ENGINE')
DB_NAME = config('DB_NAME')

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

FRONTEND_URL= config("FRONTEND_URL")
FRONTEND_EMAIL_VERIFY_URL= config("FRONTEND_EMAIL_VERIFY_URL")
 
# CORS
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['localbundy-backend.herokuapp.com', '127.0.0.1', 'localhost']
