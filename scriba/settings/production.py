import dj_database_url

from scriba.settings.base import *


ENVIRONMENT = 'production'

DEBUG = True

ALLOWED_HOSTS = [
    '178.128.41.130',
    'englishapp.tk',
    'www.englishapp.tk',
    '.herokuapp.com'
]

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

"""
DATABASES['default'] = dj_database_url.config(
    default=os.environ.get('DATABASE_URL', '')
)
"""
