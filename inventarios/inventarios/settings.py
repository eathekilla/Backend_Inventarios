"""
Django settings for inventarios project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c!ln%xnu77e9&vloqlfmi!ldz-7c76g(*hva13(#ba5f61xg*3'
X_FRAME_OPTIONS = 'ALLOWALL'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'inventarios.ottsa.online',
    'inventario.grovity.co',
    'inventarioscrecento.ottsa.online',
    '127.0.0.1',
    'localhost',
    '34.232.246.79',
    'backendappinventarios-production.up.railway.app'
]

LOGIN_URL = '/login/'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://34.232.246.79',
    'https://inventario.grovity.co',
    'https://inventarios.ottsa.online',
    'https://inventarioscrecento.ottsa.online',
    'https://backendappinventarios-production.up.railway.app'
]

CSRF_TRUSTED_ORIGINS = [
    'https://inventarioscrecento.ottsa.online',
    'https://inventarios.ottsa.online',
    'https://inventario.grovity.co',
    'https://backendappinventarios-production.up.railway.app',
    'http://127.0.0.1',
    'http://34.232.246.79'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'Entrada.apps.EntradaConfig',
    'Salida.apps.SalidaConfig',
    'Proveedor.apps.ProveedorConfig',
    'Fincas.apps.FincasConfig',
    'Insumo.apps.InsumoConfig',
    'Frontend.apps.FrontendConfig',
    'simple_history',
    'whitenoise.runserver_nostatic', 
    'django.contrib.humanize'

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'inventarios.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['inventarios/staticfiles/templates'],
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

WSGI_APPLICATION = 'inventarios.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'inventarios',
        'USER': 'postgres',
        'PASSWORD': 'vK,e9yZ20]_4',
        'HOST': 'inventarios.cxklqq1pgnsl.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }}

"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'inventarios',
        'USER': 'postgres',
        'PASSWORD': 'lPeHLqrtVsjnIJlFkDogcwsanRMxvfQJ',
        'HOST': 'roundhouse.proxy.rlwy.net',
        'PORT': '13107',
    }} 

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Si has configurado una carpeta global de archivos estáticos:
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]

# Si estás usando `collectstatic` para recopilar archivos estáticos en producción:
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),}



AWS_ACCESS_KEY_ID = 'AKIAUZKQGWNPLXZ2K27G'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'mediacrecento'
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
