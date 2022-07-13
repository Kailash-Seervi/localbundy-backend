from .base import *

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