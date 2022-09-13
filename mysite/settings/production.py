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

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://6975369468324c3baa02b389ee8dcbeb@o1380602.ingest.sentry.io/6693855",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)

#redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
# Channel layer definitions
# http://channels.readthedocs.org/en/latest/deploying.html#setting-up-a-channel-backend
CHANNEL_LAYERS = {
    "default": {
        # This example app uses the Redis channel layer implementation asgi_redis
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, 6379)],
        },
        "ROUTING": "multichat.routing.channel_routing",
    },
}


# Configure your Q cluster
# More details https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
"default": {
    "HOST": "redis",
    "PORT": "6379",
    "URL": os.getenv("REDISTOGO_URL", "redis://localhost:6379"),  # If you're
    "DB": 0,
    "DEFAULT_TIMEOUT": 480,
  }
}

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', "locahost:6379")

CELERY_BEAT_SCHEDULE = {
    # 'create_iclp_sensor_report': {
    #     'task': 'sensor.services.tasks.create_iclp_sensor_report',
    #     # execute every 15 minute with offset of 2
    #     'schedule': crontab(minute='02,17,32,47'),
    # },
    'create_tive_sensor_report': {
        'task': 'management.cron.my_scheduled_job',
        # execute every 10 minute with offset of 2
        'schedule': crontab(minute='03,13,23,33,43,53'),
    }
}
