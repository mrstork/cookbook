import os
import logging
import cssutils

PRODUCTION = bool(os.getenv('GAE_INSTANCE'))

SETTINGS_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # Application secret keys
# from libs import secrets
# SECRETS = secrets.getter(os.path.join(BASE_DIR, 'secrets.json'))
# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = SECRETS['secret_key']

SECRET_KEY = 'pf-@jxtojga)z+4s*uwbgjrq$aep62-thd0q7f&o77xtpla!_m'

if PRODUCTION:
    DEBUG = False
    DNS_ALIAS = 'www.ryorisho.com'

    # SECURITY WARNING: App Engine's security features ensure that it is safe to
    # have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a Django
    # app not on App Engine, make sure to set an appropriate host here.
    ALLOWED_HOSTS = [
        '*',
        'ryorisho.appspot.com',
        DNS_ALIAS,
    ]
else:
    DEBUG = True

    # Allow requests from localhost during development
    ALLOWED_HOSTS = [
        '127.0.0.1'
    ]

# Application definition

REQUIRED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'general',
    'public',
    'accounts',
    'recipes',
]

INSTALLED_APPS = REQUIRED_APPS + PROJECT_APPS

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
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '/cloudsql/ryorisho:us-central1:ryorisho-mysql',
        'PORT': '3306',
        'USER': 'application',
        'NAME': 'ryorisho',
        'PASSWORD': ',dNB@38$-Ue8HAJ<',
    }
}

if not PRODUCTION:
    DATABASES['default']['HOST'] = '127.0.0.1'

# Passwords
# https://docs.djangoproject.com/en/1.11/topics/auth/passwords/

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Security
# https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'

# if PRODUCTION:
#     SECURE_SSL_REDIRECT = True
#     CSRF_COOKIE_SECURE = True
#     SESSION_COOKIE_SECURE = True

# TODO: SECURE_HSTS_SECONDS
# https://docs.djangoproject.com/en/1.11/ref/middleware/#http-strict-transport-security

# Static files
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'

# Email settings
# https://github.com/anymail/django-anymail

DEFAULT_FROM_EMAIL = 'support@ryorisho.com'

# Turn off logging about unfound properties
cssutils.log.setLevel(logging.CRITICAL)

if PRODUCTION:

    INSTALLED_APPS.append('anymail')

    BASE_URL = 'http://' + DNS_ALIAS

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
# https://docs.djangoproject.com/en/1.11/ref/settings/

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
