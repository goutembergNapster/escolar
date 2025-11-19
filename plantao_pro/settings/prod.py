from .base import *
import dj_database_url
import os


DEBUG = False

ALLOWED_HOSTS = [
    "*",
    ".onrender.com",
]

# ========= DATABASE ========= #
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# ========= STATIC ========= #
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise — precisa estar entre SecurityMiddleware e tudo que usa static
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


# ========= MEDIA (Render não persiste local!) ========= #
# Para evitar erros, mantenha MEDIA_ROOT dentro do projeto.
# Render NÃO permite escrita fora do container.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"   # <-- CORRIGIDO


# ========= OUTROS ========= #
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
