"""
Configuration de développement pour Student Matching
Version sans dépendances externes pour le développement local
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jlo06u_83l4@9rb_21p4n0^d7w6at1f(-#(yvs6flbyshaw%oe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS - Ajouter les domaines pour le déploiement
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    # Ajoutez ici votre domaine de production
    # 'votredomaine.com',
    # 'www.votredomaine.com',
]

# Configuration HTTPS pour la production
SECURE_SSL_REDIRECT = False  # Mettre à True en production
SECURE_HSTS_SECONDS = 0      # Mettre à 31536000 (1 an) en production
SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # Mettre à True en production
SECURE_HSTS_PRELOAD = False  # Mettre à True en production

# Cookies sécurisés
SESSION_COOKIE_SECURE = False  # Mettre à True en production avec HTTPS
CSRF_COOKIE_SECURE = False     # Mettre à True en production avec HTTPS
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Configuration des cookies
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Sécurité des headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuration pour les fichiers statiques en production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files configuration pour la production
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Application definition

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect after login
LOGIN_REDIRECT_URL = '/'

# Redirect after logout
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Fix for Django 4.2.10 + Python 3.14 compatibility issue
import os
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')
