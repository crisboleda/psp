
# Base configurations
from psp.config.base import *
from varlocal import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zevowaa8l@qk%h+267i3lroj*j1r3-&%71b@zlx4#ww(2emly+'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
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