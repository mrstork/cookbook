# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

import os
import sys
import logging
import cssutils
from socket import gethostname

"""
Django settings for cookbook project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)
WSGI_DIR = os.path.dirname(BASE_DIR)
REPO_DIR = os.path.dirname(WSGI_DIR)
DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

sys.path.append(os.path.join(REPO_DIR, 'libs'))

# Application secret keys
import secrets
SECRETS = secrets.getter(os.path.join(DATA_DIR, 'secrets.json'))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    gethostname(),  # For internal OpenShift load balancer security purposes.
    os.environ.get('OPENSHIFT_APP_DNS'),  # OpenShift gear name.
    'www.ryorisho.com', # DNS Alias
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'anymail',
    'general',
    'public',
    'accounts',
    'recipes',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'cookbook.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'cookbook.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'db.cookbook'),
    }
}


# Passwords
# https://docs.djangoproject.com/en/1.8/topics/auth/passwords/

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Security
# https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Static files
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(WSGI_DIR, 'static')

MEDIA_ROOT=os.path.join(WSGI_DIR, 'media')
MEDIA_URL='/media/'

# Email settings
# https://github.com/anymail/django-anymail

DEFAULT_FROM_EMAIL = 'support@ryorisho.com'

# Turn off logging about unfound properties
cssutils.log.setLevel(logging.CRITICAL)

if os.environ.get('OPENSHIFT_APP_DNS'):

    BASE_URL = os.environ.get('OPENSHIFT_APP_DNS')

    ANYMAIL = {
        'MAILGUN_API_KEY': os.environ.get('MAILGUN_API_KEY'),
        'MAILGUN_SENDER_DOMAIN': 'ryorisho.com',
    }
    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

else:

    BASE_URL = 'http://127.0.0.1:8000'

    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = 'mail-logs'


# Login URLs
# https://docs.djangoproject.com/en/1.8/ref/settings/

# Login required url
LOGIN_URL = '/accounts/login'
# Successful login url
LOGIN_REDIRECT_URL = '/recipes/'

# Django Rest Framework
# http://www.django-rest-framework.org/api-guide/permissions/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    )
}

# Development environment vaues
if not os.environ.get('OPENSHIFT_APP_DNS'):
    DEBUG = True

    # Allow requests from localhost during development
    ALLOWED_HOSTS.append('127.0.0.1')
