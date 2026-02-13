# settings.py

import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url

# ------------------------------
# Chemins de base
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# Clés et debug
# ------------------------------
SECRET_KEY = config("SECRET_KEY", default="dev-secret-key")
DEBUG = config("DEBUG", default=True, cast=bool)

# ------------------------------
# Hôtes autorisés
# ------------------------------
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1", 
    "fuegodelcorazon-3.onrender.com"
]

# ------------------------------
# Applications installées
# ------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "profiles",
    "questions",
    "matching",
]

# ------------------------------
# Middleware
# ------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------
# URL racine
# ------------------------------
ROOT_URLCONF = "student_matching.urls"

# ------------------------------
# Templates
# ------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ------------------------------
# WSGI
# ------------------------------
WSGI_APPLICATION = "student_matching.wsgi.application"

# ------------------------------
# Base de données
# ------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}

# ------------------------------
# Mots de passe
# ------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------
# Localisation
# ------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------
# Fichiers statiques
# ------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------------
# Media (photos utilisateurs)
# ------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------
# Authentification
# ------------------------------
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# ------------------------------
# Sécurité
# ------------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://fuegodelcorazon-3.onrender.com",
    "https://fuegodelcorazon.onrender.com"
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ------------------------------
# Logs pour debug
# ------------------------------
if DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)
