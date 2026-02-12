"""
Django settings for student_matching project.
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ======================
# SECURITY
# ======================

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-very-important!')

# DEBUG setting pour développement local
if 'DATABASE_URL' in os.environ:
    DEBUG = config('DEBUG', default=False, cast=bool)
else:
    DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
    'fuegodelcorazon.onrender.com',
]


# ======================
# DATABASE
# ======================

# Configuration de la base de données pour Render (PostgreSQL)
# Vérification multiple pour s'assurer que PostgreSQL est utilisé en production
database_url = os.environ.get('DATABASE_URL') or os.environ.get('RENDER_DATABASE_URL')

# Force PostgreSQL si nous sommes sur Render (détection par hostname)
is_render = any('.onrender.com' in host for host in ALLOWED_HOSTS)

if database_url:
    print(f"Using PostgreSQL database: {database_url[:50]}...")
    DATABASES = {
        'default': dj_database_url.parse(database_url)
    }
elif is_render:
    # Configuration PostgreSQL manuelle pour Render (solution de secours)
    render_db_name = os.environ.get('RENDER_DB_NAME', 'fuegodelcorazon')
    render_db_user = os.environ.get('RENDER_DB_USER', 'fuegodelcorazon') 
    render_db_password = os.environ.get('RENDER_DB_PASSWORD', '')
    render_db_host = os.environ.get('RENDER_DB_HOST', 'localhost')
    render_db_port = os.environ.get('RENDER_DB_PORT', '5432')
    
    if render_db_password:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': render_db_name,
                'USER': render_db_user,
                'PASSWORD': render_db_password,
                'HOST': render_db_host,
                'PORT': render_db_port,
            }
        }
        print(f"Using PostgreSQL with manual config for Render")
    else:
        print("WARNING: No PostgreSQL credentials found, falling back to SQLite")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    print("Using SQLite database (development mode)")
    # Configuration locale (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ======================
# APPLICATIONS
# ======================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'profiles',
    'questions',
    'matching',
]


# ======================
# MIDDLEWARE
# ======================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Important pour Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'student_matching.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'student_matching.wsgi.application'


# ======================
# PASSWORD VALIDATION
# ======================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ======================
# INTERNATIONALIZATION
# ======================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ======================
# STATIC & MEDIA FILES
# ======================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ======================
# DEFAULT FIELD
# ======================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ======================
# LOGIN REDIRECTS
# ======================

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
