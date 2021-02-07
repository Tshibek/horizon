from skyhorizon.settings.common import *

SECRET_KEY = secrets['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# WINDOWS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'skyhorizons',
        'USER': 'tshibe',
        'PASSWORD': 'password',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}
# MAC
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': '127.0.0.1',
#         'PORT': '8889',
#         'NAME': 'skyhorizon',
#         'USER': 'user',
#         'PASSWORD': 'password',
#     }
# }
