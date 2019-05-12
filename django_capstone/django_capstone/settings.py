"""
Django settings for django_capstone project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Social Login


def get_env(setting, envs):
    try:
        return envs[setting]
    except KeyError:
        error_msg = "You SHOULD set {} environ".format(setting)
        raise ImproperlyConfigured(error_msg)


DEV_ENVS = os.path.join(BASE_DIR + '/Base_dir/', "envs_dev.json")
DEPLOY_ENVS = os.path.join(BASE_DIR + '/Base_dir/', "envs.json")

if os.path.exists(DEV_ENVS):  # Develop Env
    env_file = open(DEV_ENVS)
elif os.path.exists(DEPLOY_ENVS):  # Deploy Env
    env_file = open(DEPLOY_ENVS)
else:
    env_file = None

if env_file is None:  # System environ
    try:
        #FACEBOOK_KEY = os.environ['FACEBOOK_KEY']
        #FACEBOOK_SECRET = os.environ['FACEBOOK_SECRET']
        GOOGLE_KEY = os.environ['GOOGLE_KEY']
        GOOGLE_SECRET = os.environ['GOOGLE_SECRET']
    except KeyError as error_msg:
        raise ImproperlyConfigured(error_msg)
else:  # JSON env
    envs = json.loads(env_file.read())
    #FACEBOOK_KEY = get_env('FACEBOOK_KEY', envs)
    #FACEBOOK_SECRET = get_env('FACEBOOK_SECRET', envs)
    GOOGLE_KEY = get_env('GOOGLE_KEY', envs)
    GOOGLE_SECRET = get_env('GOOGLE_SECRET', envs)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8sisfla$nu#t!!8(^ti6vowf7og3sd-e5bxadjgds&zyeq#pg3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'moyak.kr',
    '0.0.0.0',
    'localhost',
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'social_django',

    # my apps
    'main',
    'dashboard',
    'upload',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',  # Google
    # 'social_core.backends.facebook.FacebookOAuth2',  # Facebook
    'django.contrib.auth.backends.ModelBackend',  # Django basic model
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # add this middleware
]

ROOT_URLCONF = 'django_capstone.urls'

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

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect'
            ],
        },
    },
]

WSGI_APPLICATION = 'django_capstone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SocialLogin: Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_SECRET

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = '/home/'
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media'),
)

# Media files (File upload)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
