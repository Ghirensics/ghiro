# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import os
from django.conf import global_settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

# Actual Ghiro release.
GHIRO_VERSION = "0.3-dev"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Disabled time zone, using local time instead.
USE_TZ = False
TIME_ZONE = None

# Project directory.
PROJECT_DIR = os.getcwd()

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.getcwd(), "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Upload handler (store only on disk).
FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.TemporaryFileUploadHandler",)

# Unique secret key generator.
# Secret key will be placed in secret_key.py file.
try:
    from ghiro.secret_key import *
except ImportError:
    SETTINGS_DIR=os.path.abspath(os.path.dirname(__file__))
    # Using the same generation schema of Django startproject.
    from django.utils.crypto import get_random_string
    key = get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")
    # Write secret_key.py
    with open(os.path.join(SETTINGS_DIR, "secret_key.py"), "w") as file:
        file.write("SECRET_KEY = \"{0}\"".format(key))
    # Reload key.
    from ghiro.secret_key import *

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    )

INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ghiro.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ghiro.wsgi.application'

TEMPLATE_DIRS = (
    "templates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'debug_toolbar',
    "users",
    "analyses",
    "hashes",
    "system",
)

# Hack to import local settings.
try:
    LOCAL_SETTINGS
except NameError:
    try:
        from .local_settings import *
    except ImportError:
        pass

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
        'management_command': {
            'format': "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        },
        'audit_formatter': {
            'format': "%(asctime)s %(message)s"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            },
        'processing': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'management_command',
            },
        # Image processing log file.
        'processing_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, LOG_PROCESSING_NAME),
            'maxBytes': LOG_PROCESSING_SIZE,
            'backupCount': LOG_PROCESSING_NUM,
            'formatter': 'management_command'
        },
        # Audit log file, it keeps logs of all users actions.
        'audit_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, LOG_AUDIT_NAME),
            'maxBytes': LOG_AUDIT_SIZE,
            'backupCount': LOG_AUDIT_NUM,
            'formatter': 'audit_formatter'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'lib': {
            'handlers': ['processing', 'processing_file'],
            'level': 'DEBUG',
            'propagate': False,
            },
        'plugins': {
            'handlers': ['processing', 'processing_file'],
            'level': 'DEBUG',
            'propagate': False,
            },
        'audit': {
            'handlers': ['audit_file'],
            'level': 'DEBUG',
        },
    }
}

# Custom user model.
AUTH_USER_MODEL = "users.Profile"
# Redirect logged users.
LOGIN_URL = "/users/login/"
LOGOUT_URL = "/users/logout/"
LOGIN_REDIRECT_URL = "/"

# Custom context processors.
TEMPLATE_CONTEXT_PROCESSORS += ("analyses.context_processors.dashboard_data",
                                "analyses.context_processors.ghiro_release")

# Create log directory.
if not os.path.exists(LOG_DIR):
    try:
        os.mkdir(LOG_DIR)
    except Exception as e:
        print("Unable to create log directory: %s" % e)
