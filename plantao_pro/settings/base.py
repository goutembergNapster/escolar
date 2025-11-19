import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Permite ler arquivo .env

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Segurança
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = bool(int(os.getenv("DEBUG", "1")))

# Backends de autenticação
AUTHENTICATION_BACKENDS = [
    "home.auth_backends.CPFBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Hosts permitidos
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()
]

# Apps instalados
INSTALLED_APPS = [
    "home",                     # APP principal
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL e WSGI
ROOT_URLCONF = "plantao_pro.urls"
WSGI_APPLICATION = "plantao_pro.wsgi.application"
ASGI_APPLICATION = "plantao_pro.asgi.application"

# Banco de dados via DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Localização
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True

# Custom User
AUTH_USER_MODEL = "home.User"

# Arquivos estáticos
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []  # NÃO use diretórios extras (evita conflito no Render)

# Arquivos de mídia (uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = Path("/data/web/media")  # compatível com Render + Docker

# ID padrão de models
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Templates (VERSÃO CORRETA)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # Diretórios personalizados — APENAS a raiz
        "DIRS": [
            os.path.join(BASE_DIR, "home", "templates"),
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "plantao_pro.context_processors.escola_no_contexto",
            ],
        },
    },
]
