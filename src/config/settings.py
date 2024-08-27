from email.policy import default
from pathlib import Path

from config.env import config

POSTGRES_LOCALLY = False  # when I want to use postgres locally
ENVIRONMENT = config("ENVIRONMENT", default="development")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!


if ENVIRONMENT == "development":
    DEBUG = True
else:
    DEBUG = False


ALLOWED_HOSTS = [
    config("RENDER_EXTERNAL_HOSTNAME"),
    config("RAILWAY_EXTERNAL_HOSTNAME"),
    "farmersreward.co",
    "www.farmersreward.co",
    "127.0.0.1",
    "localhost:8000",
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    "localhost:8000",
]


CSRF_TRUSTED_ORIGINS = [
    "https://farmers-reward-production.up.railway.app",
    "https://*.onrender.com",
    "https://*farmersreward.co",
    "https://farmersreward.co",
]

# Application definition

INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "cloudinary_storage",
    "cloudinary",
    "debug_toolbar",
    "django_extensions",
    "cities_light",
    "admin_honeypot",
    # User defined apps
    "core",
    "farmers",
    "market",
    "subsidy",
    "vendors",
    "waitlist",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# from .db import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Production database configuration from environment variables
DATABASE_URL = config("DATABASE_URL", default=None)


if ENVIRONMENT == "production" or POSTGRES_LOCALLY == True:
    import dj_database_url

    DATABASE_URL = str(DATABASE_URL)
    print(f"Using production database: {DATABASE_URL}")
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=30,
            conn_health_checks=True,
        )
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"


if ENVIRONMENT == "production" or POSTGRES_LOCALLY == True:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
else:
    MEDIA_ROOT = BASE_DIR / "media"


CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDIDARY_API_KEY"),
    "API_SECRET": config("CLOUDIDARY_SECRET_KEY"),
}


# WhiteNoise
# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }


# Base url to serve media files
MEDIA_URL = "media/"

# Path where media is stored'
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cities Light configuration
CITIES_LIGHT_TRANSLATION_LANGUAGES = ["en"]  # Set the translation languages
CITIES_LIGHT_INCLUDE_COUNTRIES = ["NG"]
CITIES_LIGHT_INCLUDE_CITY_TYPES = ["PPL"]  # Include specific city types
CITIES_LIGHT_APP = "core"
AUTH_USER_MODEL = "core.User"


# Gmail Smtp configuration

# default backend
if ENVIRONMENT == "production" or POSTGRES_LOCALLY == True:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = config("EMAIL_HOST", cast=str, default=None)
    EMAIL_PORT = config("EMAIL_PORT", cast=str, default="587")  # Recommended
    EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str, default=None)
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str, default=None)
    EMAIL_USE_TLS = config(
        "EMAIL_USE_TLS", cast=bool, default=True
    )  # Use EMAIL_PORT 587 for TLS
    # EMAIL_USE_SSL = config("EMAIL_USE_TLS", cast=bool, default=False)  # EUse MAIL_PORT 465 for SSL
    DEFAULT_FROM_EMAIL = f'FarmersReward {config("ADMIN_USER_EMAIL")}'
    ACCOUNT_EMAIL_SUBJECT_PREFIX = ""

else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Admin settings.py
UNFOLD = {
    "SITE_HEADER": "Farmers Reward",
    "SITE_URL": "/",
    "SHOW_HISTORY": False,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
}
