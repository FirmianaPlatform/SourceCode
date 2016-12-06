# Django settings for firmiana project.
import os
_ROOT_PATH = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

#ALLOWED_HOSTS = '*'

#AUTH_USER_MODEL = "experiments.NewUser"

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
     ('firmiana', 'proteome.firmiana@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'galaxy',                      # Or path to database file if using sqlite3.
        'USER': 'phoenix',                      # Not used with sqlite3.
        'PASSWORD': 'firmianaadmin',                  # Not used with sqlite3.
        #'HOST': '61.50.134.132',                      # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '192.168.99.201', 
        'PORT': '6032',                   # Set to empty string for default. Not used with sqlite3.
       # 'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;' }
    },
    #'galaxydb': {
      #  'NAME': 'galaxy',
       # 'ENGINE': 'django.db.backends.mysql',
       # 'USER': 'root',
       # 'PASSWORD': '12345'
    #}
    'responders_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'script_map',                      # Or path to database file if using sqlite3.
        'USER': 'phoenix',                      # Not used with sqlite3.
        'PASSWORD': 'firmianaadmin',                  # Not used with sqlite3.
        'HOST': '10.1.8.210',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '6033',                   # Set to empty string for default. Not used with sqlite3.
       # 'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;' }
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

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

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT =  _ROOT_PATH+'/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/usr/local/firmiana/leafy/static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(_ROOT_PATH, 'static'),    #project-wide static files            
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1b6=ebva96!o3)^3$jf6#(=*#lqh$naj-cf&j+wjkym&8^svf&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (                   
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.eggs.Loader',

)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'leafy.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'leafy.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(_ROOT_PATH, 'templates'), #project-wide templates 
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',  
    #'django_like',  
    'experiments',
    #'msanalysis',
    #'display',
    #'LFQuantViewer',
    'gardener',
    'responders',
    
    #'galaxyui',
    #'infinity'#infinity just for test jsgrid
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'proteome.firmiana@gmail.com'
EMAIL_HOST_PASSWORD = 'ecnufirmiana'
EMAIL_USE_TLS = True

DATABASE_ROUTERS = ['responders.router.RespondersRouter']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '0.0.0.0:11211',
    }
}

#CACHE_MIDDLEWARE_ALIAS=default
CACHE_MIDDLEWARE_SECONDS=60
CACHE_MIDDLEWARE_KEY_PREFIX='' 



##Custom Parameters
DJANGO_DISPLAY="/gardener/"
LOGOUT_PAGE = "/login/"
LOGIN_PAGE  = "/login/"

GALAXY_ID_SECRET = "12345"
GALAXY_ROOT="/usr/local/firmiana/galaxy-dist/"
#GALAXY_URL="61.50.134.132:8080"
GALAXY_URL="192.168.99.201:8080"
GALAXY_URL_LOGIN = GALAXY_URL + '/galaxy/user/login/'
#GALAXY_URL_LOGIN='http://61.50.134.132/galaxy/user/login/'
GALAXY_LIB_PATH= os.path.join(GALAXY_ROOT, 'lib')
GALAXY_EGG_PATH=os.path.join(GALAXY_ROOT, 'eggs')

