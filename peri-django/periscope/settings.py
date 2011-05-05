# Django settings for periscope project.
import os
import logging
import logging.handlers

DEBUG = True
TEMPLATE_DEBUG = DEBUG

try:
    PERISCOPE_ROOT = os.environ['PERISCOPE_ROOT']
except:
    PERISCOPE_ROOT = os.path.dirname(os.path.abspath(__file__)) + os.sep
    
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# AH: ESNet's topology is much larger, it's better to use mysql5.0+

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': PERISCOPE_ROOT + 'database/periscope.sqlite',  # Or path to database file if using sqlite3.
#        'USER': '',                      # Not used with sqlite3.
#        'PASSWORD': '',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#        'OPTIONS': { 'timeout': 20 },
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'periscopedb',  # Or path to database file if using sqlite3.
        'USER': 'periuser',                      # Not used with sqlite3.
        'PASSWORD': 'peri2pass',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': { "init_command": "SET storage_engine=INNODB",} # for supporting transactions and foreign keys
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

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
MEDIA_ROOT = PERISCOPE_ROOT + 'static_media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7g#y6wiqv0cd4g8q&h!di&t7xr3q-5#-2t1n^%#t8)mwxbxhml'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'periscope.urls'

TEMPLATE_DIRS = (
    PERISCOPE_ROOT + 'templates',
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'periscope.topology',
    'periscope.monitoring',
    'periscope.measurements',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
)

# The location to save the topology SVG file
TOPOLOGY_SVG = '/tmp/topology.svg'


# Hints URL for perfSONAR root gLSes (can be http:// or file://)
GLS_ROOT_HINTS = 'http://www.perfsonar.net/gls.root.hints'

# The log file full path for periscope
LOG_FILE = '/tmp/periscope' # better to use /var/log but needs permissions on the file

# Setup a logger for periscope
logger = logging.getLogger('periscope')
if len(logger.handlers) == 0:
    hdlr = logging.handlers.RotatingFileHandler(
              LOG_FILE , maxBytes=5242880, backupCount=5)
    #formatter = logging.Formatter('%(lineno)s %(asctime)s %(levelname)s %(message)s')
    formatter = logging.Formatter('%(name)s :%(asctime)s %(filename)s %(lineno)s %(levelname)s  %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
