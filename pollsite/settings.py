"""
Django settings for pollsite project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5m3ufe=_orsml&icqretoy-mkat@yai16qbz7djwv*zty5t^5b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
#---------------------------------------------------------------
#- Default django applications to be used within this project.
#- See comments below:
INSTALLED_APPS = (
    'django.contrib.admin',         #- Admin site for developers.
    'django.contrib.auth',          #- An authentication system.
    'django.contrib.contenttypes',  #- Allows permissions to be associated with models.
    'django.contrib.sessions',      #- A session framework                   (?)
    'django.contrib.messages',      #- Allows using flash-massaging across views (recommended with redirect requests)
    'django.contrib.staticfiles',   #- A framework for managing static files (?)
    'polls'                         #- This is the application I created to handle the polls.
)
#- Some of this applications run on database(s) that need to be
#- built before continue, so the following command is needed
#-
#- $python manage.py migrate
#-
#- in order to create needed databeases according to settings
#- specifications.
#---------------------------------------------------------------

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',            #- manages sessions across requests.
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',         #- associates users with requests using sessions.
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',  #- logs users out after changing the password.
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'pollsite.urls'
LOGIN_URL = "polls:login"
LOGOUT_URL = "polls:logout"
LOGIN_REDIRECT_URL = "polls:index"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],                   #- Adding templates directory
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

WSGI_APPLICATION = 'pollsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
#---------------------------------------------------------------
#- For testing sqllite is OK, but it's RECOMMENDED to use a more
#- robust database when going live!
#- When using PostgreSQL or MySQL additional settings might be
#- required (USER, PASSWORD, HOST), further, after the creation
#- of the project (django-admin startproject name) the database
#- needs to be created. This is not needed when using SQLite.
#---------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

#- Set my timezone here!
TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
