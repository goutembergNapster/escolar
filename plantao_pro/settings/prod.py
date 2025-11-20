from .base import *
import os
import dj_database_url

DEBUG = False

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL")
    )
}

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
