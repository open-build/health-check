from .base import *
import os
from os.path import join, normpath

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'health',
        'PASSWORD': os.environ.get("PASSWORD"),
        'USER': 'health',
        'HOST': 'db-mysql-nyc3-97229-do-user-2508039-0.b.db.ondigitalocean.com',
        'PORT': '25060',
    }
}

DEBUG = False

ALLOWED_HOSTS = ['seahorse-app-mrqwo.ondigitalocean.app', 'open.build', '127.0.0.1', '[::1]','health.open.build',]

try:
    from .local import *
except ImportError:
    pass

CRON_JOBS = {
    'cron': '*/5 * * * *'
}
