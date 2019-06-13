"""
Django settings for django_airavata_gateway project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

from pkg_resources import iter_entry_points

from django_airavata.app_config import enhance_custom_app_config

from . import webpack_loader_util

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bots0)m91u_i4gpw+103o%2jn#j57wjh7s@9$x*27_4^*jyku4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
INTERNAL_IPS = ["127.0.0.1"]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django_airavata.apps.admin.apps.AdminConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_airavata.apps.auth.apps.AuthConfig',
    'django_airavata.apps.workspace.apps.WorkspaceConfig',
    'rest_framework',
    'django_airavata.apps.api.apps.ApiConfig',
    'django_airavata.apps.groups.apps.GroupsConfig',
    'django_airavata.apps.dataparsers.apps.DataParsersConfig',

    # wagtail related apps
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    # wagtail third party dependencies
    'modelcluster',
    'taggit',
    'wagtailfontawesome',

    # wagtail custom apps
    'django_airavata.wagtailapps.base.apps.BaseConfig',

    # django-webpack-loader
    'webpack_loader',
]

# AppConfig instances from custom Django apps
CUSTOM_DJANGO_APPS = []

# Add any custom apps installed in the virtual environment
# Essentially this looks for the entry_points metadata in all installed Python packages. The format of the metadata in setup.py is the following:
#
#    setuptools.setup(
#        ...
#        entry_points="""
#    [airavata.djangoapp]
#    dynamic_djangoapp = dynamic_djangoapp.apps:DynamicDjangoAppConfig
#    """,
#        ...
#    )
#
for entry_point in iter_entry_points(group='airavata.djangoapp'):
    custom_app = enhance_custom_app_config(entry_point.load())
    CUSTOM_DJANGO_APPS.append(custom_app)
    # Create path to AppConfig class (otherwise the ready() method doesn't get
    # called)
    INSTALLED_APPS.append("{}.{}".format(entry_point.module_name,
                                         entry_point.attrs[0]))

OUTPUT_VIEW_PROVIDERS = {}
for entry_point in iter_entry_points(group='airavata.output_view_providers'):
    OUTPUT_VIEW_PROVIDERS[entry_point.name] = entry_point.load()()

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_airavata.apps.auth.middleware.authz_token_middleware',
    'django_airavata.middleware.airavata_client',
    'django_airavata.middleware.sharing_client',
    'django_airavata.middleware.profile_service_client',
    # Needs to come after authz_token_middleware, airavata_client and
    # profile_service_client
    'django_airavata.apps.auth.middleware.gateway_groups_middleware',
    # Wagtail related middleware
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'django_airavata.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "django_airavata", "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_airavata.context_processors.airavata_app_registry',
                'django_airavata.context_processors.custom_app_registry',
                # 'django_airavata.context_processors.resolver_match',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_airavata.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "django_airavata", "static")]

# Media Files (PDF, Documents, Custom Images)
MEDIA_ROOT = os.path.join(BASE_DIR, "django_airavata", "media")
MEDIA_URL = '/media/'

# Data storage
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o777

# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'EXCEPTION_HANDLER':
        'django_airavata.apps.api.exceptions.custom_exception_handler',
}

AUTHENTICATION_BACKENDS = [
    'django_airavata.apps.auth.backends.KeycloakBackend'
]

# Default email backend (for local development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Wagtail related stuff
WAGTAIL_SITE_NAME = 'Django Airavata Portal'

WAGTAILIMAGES_JPEG_QUALITY = 100


LOGIN_URL = 'django_airavata_auth:login'
LOGIN_REDIRECT_URL = 'django_airavata_workspace:dashboard'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_OPTIONS = {
    # Control whether username/password authentication is allowed
    'password': {
        'name': 'your account',
    },
    # Can have multiple external logins
    # 'external': [
    #     {
    #         'idp_alias': 'cilogon',
    #         'name': 'CILogon',
    #     }
    # ]
}

# Seconds each connection in the pool is able to stay alive. If open connection
# has lived longer than this period, it will be closed.
# (https://github.com/Thriftpy/thrift_connector)
THRIFT_CLIENT_POOL_KEEPALIVE = 10

# Webpack loader
WEBPACK_LOADER = webpack_loader_util.create_webpack_loader_config()

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django_airavata': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO'
        },
    },
}

# Allow all settings to be overridden by settings_local.py file
try:
    from django_airavata.settings_local import *  # noqa
except ImportError:
    pass
