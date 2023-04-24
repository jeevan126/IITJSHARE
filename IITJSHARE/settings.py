"""
Django settings for Arcxival project.
Generated by 'django-admin startproject' using Django 2.2.2.
For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g9z1%-lllw&amvgft)hc^z0tluhlmzvouop9vm1a(saw=ny1_r'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# Application definition

INSTALLED_APPS = [
    'teacher.apps.TeacherConfig',
    'student.apps.StudentConfig',
    'customuser.apps.CustomuserConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

AUTH_USER_MODEL = 'customuser.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'IITJSHARE.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'IITJSHARE.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
MYSQL_URL = "mysql://root:cezYfOMWibyxO7mFErxO@containers-us-west-80.railway.app:6603/railway"
MYSQLDATABASE = "railway"
MYSQLHOST = "containers-us-west-80.railway.app"
MYSQLPASSWORD = "cezYfOMWibyxO7mFErxO"
MYSQLPORT = 6603
MYSQLUSER = "root"







import os
import dj_database_url

from dotenv import load_dotenv
env_file = os.path.join(BASE_DIR, 'my_env.env')
load_dotenv(env_file)


DATABASES = {
    "default": dj_database_url.config(default=os.environ.get('DATABASE_URL'), conn_max_age=1800),
    
}
# "ENGINE": "django.db.backends.mysql",
        # 'NAME': os.getenv('MYSQLDATABASE'),
        # 'USER': os.getenv('MYSQLUSER'),
        # 'PASSWORD': os.getenv('MYSQLPASSWORD'),
        # 'HOST': os.getenv('MYSQLHOST'),
        # 'PORT': os.getenv('MYSQLPORT'),
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'sql_mode': 'traditional',
#         },
#         'NAME': 'IITJSHARE',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'USER': 'root',
#         'PASSWORD': 'Jeevan#510',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/    '
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    #os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_AUTO_FIELD='django.db.models.AutoField'



EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = (os.environ.get('EMAIL_PORT'))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
