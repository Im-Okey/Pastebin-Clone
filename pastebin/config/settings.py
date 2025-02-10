import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-taw4#7_4vtsl2me*=6%!i!e*9$m!85+a#a)zx3rge5$i^4_b-v'

DEBUG = True

ALLOWED_HOSTS = ['*']

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
            'hosts': [('127.0.0.1', 6379)],
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
        'NAME': 'PastebinService',  # Название базы данных
        'USER': 'postgres',      # Имя пользователя
        'PASSWORD': 'root',  # Пароль
        'HOST': '127.0.0.1', # Адрес хоста
        'PORT': '5432',      # Порт PostgreSQL
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = "/"

AUTH_USER_MODEL = 'users.CustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
"""Удаление пасты раз в час. Удаление уведомлений раз в день. Письмо на почту раз в неделю"""
CELERY_BEAT_SCHEDULE = {
    'delete_expired_pastes_every_minute': {
        'task': 'blog.tasks.delete_expired_pastes',
        'schedule': 60.0,
    },
    'delete_old_unread_messages_and_notifications_every_minute': {
        'task': 'blog.tasks.delete_old_unread_messages_and_notifications',
        'schedule': 86400.0,
    },
    'send_weekly_unread_report': {
        'task': 'blog.tasks.send_weekly_unread_report',
        'schedule': 604800.0,
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'arseny.butko771@gmail.com'
EMAIL_HOST_PASSWORD = 'tmkzqejeveeninfe'