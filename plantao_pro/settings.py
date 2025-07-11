from pathlib import Path
import os
from django.contrib.messages import constants as messages

AUTH_USER_MODEL = 'home.User'
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-&3d@0w2x0^@2juw_v478r0h_4rk6)iv_*o6r&hc0#eq!)th3&y'
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1','0.0.0.0','*']

AUTHENTICATION_BACKENDS = [
    'home.auth_backends.CPFBackend',  # backend por CPF
    'django.contrib.auth.backends.ModelBackend',  # fallback (username etc)
]

CSRF_TRUSTED_ORIGINS = ['https://clinica-medica-i66x.onrender.com','http://clinica-medica-i66x.onrender.com']

INSTALLED_APPS = [
    'home',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'plantao_pro.middleware.verificar_escola.VerificaEscolaMiddleware',
        
]

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
ROOT_URLCONF = 'plantao_pro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'home', 'templates/plantaopro/pages')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'plantao_pro.context_processors.escola_no_contexto',
            ],
        },
    },
]

WSGI_APPLICATION = 'plantao_pro.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'escolinha_db',
        'USER': 'admin',
        'PASSWORD': '34587895',
        'HOST': 'psql',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',  # Você pode mudar para 'INFO' em produção
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, '/data/web/media')

if not DEBUG:
    
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

STATICFILES_DIRS = [
     os.path.join(BASE_DIR, 'home/static')
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
