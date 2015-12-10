import os

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_URL = dj_database_url.config()

SECRET_KEY = 'hv)#1dl326wt$bq0ujbj37d$f4$-vx^46z!n_%nn@&m4wmnsns'

DEBUG = os.environ.get('DEBUG', 'true') == 'true'

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = (
    '127.0.0.1',
)

# Application definition

INSTALLED_APPS = (
    'custom_commands',
    'modeltranslation',
    'solo',
    'colorfield',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'pages',
    'catalog',
)

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

ROOT_URLCONF = 'harmonic.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'harmonic.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DATABASES['default'].update(DB_URL)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

# translations
gettext = lambda s: s
LANGUAGES = (
    ('fr', gettext('Français')),
    ('en', gettext('English')),
)
