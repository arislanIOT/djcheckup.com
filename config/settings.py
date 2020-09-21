"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from pathlib import Path

from django.contrib.messages import constants as messages

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Dotenv support
# Django-environ support
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

env = environ.Env(
    # set casting, default value
    SECRET_KEY=(str, "this_is_just_a_temporary_secret_key"),
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, ["127.0.0.1"]),
    SENTRY_ENVIRONMENT=(str, "development"),
    SENTRY_DSN=(str, ""),
    EMAIL_HOST=(str, ""),
    EMAIL_PORT=(str, ""),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_USE_TLS=(bool, True),
    DEFAULT_FROM_EMAIL=(str, ""),
    REDIS_HOST=(str, "localhost"),
    REDIS_PORT=(int, 6379),
    REDIS_DB=(int, 0),
    REDIS_DEFAULT_TIMEOUT=(int, 3600),
    REDIS_PASSWORD=(str, ""),
    ADMIN_URL=(str, "admin"),
    USE_S3=(bool, False),
    AWS_ACCESS_KEY_ID=(str, ""),
    AWS_SECRET_ACCESS_KEY=(str, ""),
    AWS_STORAGE_BUCKET_NAME=(str, ""),
    AWS_S3_CUSTOM_DOMAIN=(str, ""),
    DB_ENGINE=(str, "django.db.backends.sqlite3"),
    DB_NAME=(str, BASE_DIR / "db.sqlite3"),
    DB_USER=(str, ""),
    DB_PASSWORD=(str, ""),
    DB_HOST=(str, ""),
    DB_PORT=(str, ""),
)

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    environment=env("SENTRY_ENVIRONMENT"),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

ADMIN_URL = env("ADMIN_URL")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # Required and added for django-allauth
    "allauth",  # Required and added for django-allauth
    "allauth.account",  # Required and added for django-allauth
    "crispy_forms",  # Required and added for django-crispy-forms
    "django_rq",  # Required and added for Django-RQ
    "storages",  # Required and added for Django-Storages
    "checks.apps.ChecksConfig",
    "website.apps.WebsiteConfig",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",  # Required and added for django-debug-toolbar
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",  # noqa Required and added for django-debug-toolbar
    ]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Pacific/Auckland"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

USE_S3 = env("USE_S3")

if USE_S3:
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_OBJECT_PARAMETERS = {"ACL": "public-read", "CacheControl": "max-age=86400"}
    if env("AWS_S3_CUSTOM_DOMAIN"):
        AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
    else:
        AWS_S3_CUSTOM_DOMAIN = f"s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}"
    AWS_LOCATION = ""
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"

else:
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# django-allauth configuration
SITE_ID = 1
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False


# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")


# django-debug-toolbar
INTERNAL_IPS = ["127.0.0.1"]


# django-crispy-forms configuration
CRISPY_TEMPLATE_PACK = "bootstrap4"


# The following constants let us use Bootstrap alerts with messages
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}


# Media
MEDIA_ROOT = "media"
MEDIA_URL = "/media/"


# Django-RQ Configuration
RQ_SHOW_ADMIN_LINK = True
RQ_QUEUES = {
    "checks": {
        "HOST": env("REDIS_HOST"),
        "PORT": env("REDIS_PORT"),
        "DB": env("REDIS_DB"),
        "DEFAULT_TIMEOUT": env("REDIS_DEFAULT_TIMEOUT"),
        "PASSWORD": env("REDIS_PASSWORD"),
    },
}


# Logging
if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "rq_console": {
                "format": "%(asctime)s %(message)s",
                "datefmt": "%H:%M:%S",
            },
            "rich": {"datefmt": "[%X]"},
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "rich.logging.RichHandler",
                "formatter": "rich",
            },
            "rq_console": {
                "level": "DEBUG",
                "class": "rich.logging.RichHandler",
                "formatter": "rich",
            },
        },
        "loggers": {
            "django": {"handlers": ["console"]},
            "rq.worker": {"handlers": ["rq_console"], "level": "DEBUG"},
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    }
