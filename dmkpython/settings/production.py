from .base import *
from django.conf import os

DEBUG = True
ALLOWED_HOSTS = ['api.digimkey.com','13.127.247.113']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'dpy',
        'USER': get_secret("DB_USER"),
        'PASSWORD': get_secret("DB_PASS"),
        # 'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        # 'PORT': '3306',
    }
}

# import pdb;pdb.set_trace()
# STATIC_URL = '/static/'
# # STATIC_ROOT = str(BASE_DIR / 'static')

# STATICFILES_DIRS = (
#     str(BASE_DIR)+'/static/',
# )

STATIC_PATH = os.path.join(str(BASE_DIR),'static')
STATIC_URL = '/static/' # You may find this is already defined as such. 
STATICFILES_DIRS = ( STATIC_PATH, )

MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / 'media')

CORS_ORIGIN_WHITELIST = ()
