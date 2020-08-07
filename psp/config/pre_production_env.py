
# Base configurations
from psp.config.base import *

# Libraries
import dj_database_url
from decouple import config


DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['*']

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'media')

MAILJET_API_KEY = config('MAILJET_API_KEY')
MAILJET_API_SECRET = config('MAILJET_API_SECRET')

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
