from scriba.settings.base import *


# local

ENVIRONMENT = 'local'

DEBUG = True

ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
    'localhost'
]

INSTALLED_APPS = INSTALLED_APPS + [
    'sslserver'
]
