"""Development settings."""
from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Use SQLite for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# CORS — allow all in dev
CORS_ALLOW_ALL_ORIGINS = True

# Show emails in console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Django Debug Toolbar (optional, install separately)
INTERNAL_IPS = ["127.0.0.1"]
