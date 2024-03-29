"""
Django settings for News_Portal project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()

import redis


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c42=h6j)e7&np&lom&*bdv0o&+o@r%r25zb32$$=pt2+v0#4un'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'News.apps.NewsConfig',
    'sign',
    'protect',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_filters',
    'django_apscheduler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'News_Portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'News', 'templates', 'flatpages')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'News_Portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/news/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

SITE_URL = 'http://127.0.0.1:8000'

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
ACCOUNT_FORMS = {'signup': 'sign.models.BasicSignupForm'}

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = 'redis://default:9LOHinVUqJigjsEaIkT668Mx06x83nt4@redis-19835.c300.eu-central-1-1.ec2.cloud.redislabs.com:19835'
CELERY_RESULT_BACKEND = 'redis://default:9LOHinVUqJigjsEaIkT668Mx06x83nt4@redis-19835.c300.eu-central-1-1.ec2.cloud.redislabs.com:19835'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}

ADMINS = [
    ('admin', os.getenv('DEFAULT_FROM_EMAIL')),
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

    'formatters': {
        'console_debug': {
            'format': '[{asctime}] / {levelname} \n'
                      '{message} \n',
            'style': '{',
        },
        'mail_error_and_console_warning': {
            'format': '[{asctime}] / {levelname} \n'
                      '{pathname} \n'
                      '{message} \n',
            'style': '{',
        },
        'errors_log_error_and_console_error': {
            'format': '[{asctime}] / {levelname} \n'
                      '{exc_info} \n'
                      '{pathname} \n'
                      '{message} \n',
            'style': '{',
        },
        'security_log_and_general_log_info': {
            'format': '[{asctime}] / {levelname} \n'
                      '{module} \n'
                      '{message} \n',
            'style': '{',
        },
    },

    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_debug',
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'mail_error_and_console_warning',
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'errors_log_error_and_console_error',
        },
        'general_log_info': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR}/logs/general.log',
            'formatter': 'security_log_and_general_log_info',
        },
        'errors_log_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR}/logs/errors.log',
            'formatter': 'errors_log_error_and_console_error',
        },
        'security_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR}/logs/security.log',
            'formatter': 'security_log_and_general_log_info',
        },
        'mail_error': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mail_error_and_console_warning',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console_debug',
                         'console_warning',
                         'console_error',
                         'general_log_info'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['errors_log_error',
                         'mail_error'],
            'level': 'ERROR',
        },
        'django.server': {
            'handlers': ['errors_log_error',
                         'mail_error'],
            'level': 'ERROR',
        },
        'django.template': {
            'handlers': ['errors_log_error'],
            'level': 'ERROR',
        },
        'django.db.backends': {
            'handlers': ['errors_log_error'],
            'level': 'ERROR',
        },
        'django.security': {
            'handlers': ['security_log'],
            'level': 'DEBUG',
        },
    },
}


