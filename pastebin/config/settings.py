import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(" ")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'django_celery_beat',
    'django_celery_results',
    'channels',
    "debug_toolbar",

    # my apps
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'general.apps.GeneralConfig',
    'subscriptions.apps.SubscriptionsConfig',
    'notifications.apps.NotificationsConfig',
]

ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.getenv('REDIS_HOST'), os.getenv('REDIS_PORT'))],
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'general.context_processors.unread_counts',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Other settings
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = "/"
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

# Authentication
AUTH_USER_MODEL = 'users.CustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# Celery
CELERY_BROKER_URL = f"redis://{os.getenv('CELERY_HOST')}:{os.getenv('CELERY_PORT')}/0"
CELERY_ACCEPT_CONTENT = os.getenv('CELERY_ACCEPT_CONTENT').split(" ")
CELERY_TASK_SERIALIZER = os.getenv('CELERY_TASK_SERIALIZER')
CELERY_RESULT_BACKEND = f"redis://{os.getenv('CELERY_HOST')}:{os.getenv('CELERY_PORT')}/0"
CELERY_BEAT_SCHEDULE = {
    'delete_expired_pastes_every_minute': {
        'task': 'blog.tasks.delete_expired_pastes',
        'schedule': 60.0,
    },
    'delete_old_unread_messages_and_notifications_every_minute': {
        'task': 'blog.tasks.delete_old_unread_messages_and_notifications',
        'schedule': 60.0,  # 86400.0
    },
    'send_weekly_unread_report': {
        'task': 'blog.tasks.send_weekly_unread_report',
        'schedule': 60.0,  # 604800.0
    },
}
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

# Email settings
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").lower() == "true"
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


INTERNAL_IPS = [
    '127.0.0.1',
]