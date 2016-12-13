#coding: utf-8

"""
Django settings for blogbootstrap project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# coding utf-8
import os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BASEFILE = '/home/cpuloader/blogbs/bin/filetocopy.zip'
BASEDICT = '/home/cpuloader/blogbs/bin/basedict.txt'

LOGIN_REDIRECT_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1f5$aczt14((1u^$bz)$rp7(&!)4y_(nt9d1olzw1m7ayvpq1o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['cpuloader.pythonanywhere.com']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'disqus',
    'carousel',
    'soundtracks',
    'tempurls',
    'anymail',
    'speaker',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'blogbootstrap.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogbootstrap.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cpuloader$blogbs',
        'USER': 'cpuloader',
        'PASSWORD':'volosatiy0',
        'HOST': 'cpuloader.mysql.pythonanywhere-services.com', 
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru'
LANGUAGES = (
	('ru', _(u'Русский')), # Python 2
	('en', _('English')),
)
LOCALE_PATHS = (
	os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SITE_ID = 1

#ADMINS = (("bols", "bols@mail.ru"), )
#MANAGERS = (("bols", "bols@mail.ru"), )

#EMAIL_HOST = "smtp.mail.ru"
#EMAIL_HOST_USER = "bols@mail.ru"
#EMAIL_HOST_PASSWORD = "neebivola"
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#DEFAULT_FROM_EMAIL = "Bols <bols@mail.ru>"

ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "MAILGUN_API_KEY": "key-8668f638ba7f7229bbc457863d303ca2",
    "MAILGUN_SENDER_DOMAIN": 'sandbox3debeca907c54d94bd4edc1548d5f2d3.mailgun.org',
}

DEFAULT_FROM_EMAIL = "postmaster@sandbox3debeca907c54d94bd4edc1548d5f2d3.mailgun.org"
EMAIL_BACKEND = 'anymail.backends.mailgun.MailgunBackend'


DISQUS_WEBSITE_SHORTNAME = 'blog-kz8i2cpqvz'
