"""
Django settings for Heroku Polls sample project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import environ

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False), )
env.read_env(env_file=root('.env'))

BASE_DIR = root()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
LOGGING_ENABLED = env.bool('LOGGING_ENABLED', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


LOCAL = [
    'django_extensions',
]

PRODUCTION = [
    'django_s3_storage',
]

COMMON = [
    'rest_framework',
    'corsheaders',
]

APPS = [
    'polls.apps.PollsConfig',
    'products.apps.ProductsConfig',
]

INSTALLED_APPS = [
    'config.apps.SuitConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_simple_bulma',
    'mathfilters',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
] + COMMON + APPS

STATICFILES_FINDERS = [
  # First add the two default Finders, since this will overwrite the default.
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',

  # Now add our custom SimpleBulma one.
  'django_simple_bulma.finders.SimpleBulmaFinder',
]

if DEBUG:
    INSTALLED_APPS += LOCAL

if not DEBUG:
    INSTALLED_APPS += PRODUCTION


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'products.context_processors.global_variables'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': env.db(default='postgres://postgres:postgres@db:5432/postgres',)
}


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}


CORS_ORIGIN_WHITELIST = [
    "https://lr-prd.herokuapp.com",
    "https://lr-uat.herokuapp.com"
]


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


LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]


if not DEBUG:
    DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
    STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
    AWS_REGION = env('AWS_REGION')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET_NAME_STATIC = env('AWS_S3_BUCKET_NAME_STATIC')
    AWS_S3_BUCKET_AUTH_STATIC = False

STATIC_URL = '/static/'
STATIC_ROOT = (root - 1)('static')

MEDIA_URL = '/media/'
MEDIA_ROOT = (root - 1)('media')
THUMB_SIZE = (120, 80)

#Auth
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


ACCOUNT_FORMS = {
    'signup': 'products.forms.CustomSignupForm',
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Allauth setup
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=1
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400
ACCOUNT_LOGOUT_REDIRECT_URL ='/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/add-address/'

if LOGGING_ENABLED:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                 'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            },
        },
    }
