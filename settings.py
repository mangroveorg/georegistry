# Django settings for georegistry project.
import os, sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Alan Viars', 'your_email@domain.com'),
)

MANAGERS = ADMINS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://b4b.s3.amazonaws.com/media/'
#http://physique7.s3.amazonaws.com/
MEDIA_URL = 'http://127.0.0.1:8000/site_media/'



MEDIASYNC = {
    'BACKEND': 'mediasync.backends.s3',
    'AWS_KEY': "125PVS8477V1GR75H2sdfdsf",
    'AWS_SECRET': "FvZLqApBXmlBw9QsdfsdfLaDJRtVm3YZTPkkjOJm",
    'AWS_BUCKET': "changethis",
}
MEDIASYNC['SERVE_REMOTE'] = False


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'
ADMIN_MEDIA_PREFIX = 'http://videntitystatic.s3.amazonaws.com/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^raoqm_qssw9fe&^rypocer5m@6dif2jfey^yr@64be*3c+1ym'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


AUTH_PROFILE_MODULE = 'accounts.UserProfile'

AUTHENTICATION_BACKENDS = ('georegistry.accounts.auth.HTTPAuthBackend',
                           'georegistry.accounts.auth.EmailBackend',
                           'django.contrib.auth.backends.ModelBackend',
                           )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
)

ROOT_URLCONF = 'georegistry.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'xform_manager/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'georegistry.features',
    'simple_locations',
    'mptt',
    'registration',
    'mediasync',
    'georegistry.accounts',
    'georegistry.sinceindex',
    'georegistry.webhook',
    #'xform_manager',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
)


API_AUTH_REQUIRED = True

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DB_NAME = "georegistry05"
MONGO_HISTORYDB_NAME = "history"
MONGO_VERIFIEDDB_NAME = "verified"


ACCOUNT_ACTIVATION_DAYS = 2
RESTRICT_REG_DOMAIN_TO = None
MIN_PASSWORD_LEN = 8

EMAIL_HOST = 'smtp.bizmail.yahoo.com'
EMAIL_PORT = 587 #25 by default
EMAIL_HOST_USER = 'no-reply@videntity.com'
EMAIL_HOST_PASSWORD = 'mypassword'