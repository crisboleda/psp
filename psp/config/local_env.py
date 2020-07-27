
# Base configurations
from psp.config.base import *


DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zevowaa8l@qk%h+267i3lroj*j1r3-&%71b@zlx4#ww(2emly+'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'psp',
        'USER': 'postgres',
        'PASSWORD': 'toor',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'local_emails')
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'emailTesting@gmail.com'
EMAIL_HOST_PASSWORD = 'testing123'
EMAIL_USE_TLS = True


STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'