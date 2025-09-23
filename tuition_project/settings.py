import os
from pathlib import Path
import socket

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-gsutf%$^_2g(*!2@6dj-@rn_z2_sj)e!5#@-4w#muq#u+2r#eq'
DEBUG = True

ALLOWED_HOSTS = [
    'sajidiqbal.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'widget_tweaks',
    'crispy_forms',
    'crispy_bootstrap5',

  # Allauth apps
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # 👇 Providers
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',

    # Local apps
    'pages',
    'Home',
    'users',
    'courses',
    'Tutor',
    'student',
    'payments',
    'live_classes',
    'assignments',
    'contact',
    'Notification',
]

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # 👇 Add this new middleware (required by allauth >= 65)
    'allauth.account.middleware.AccountMiddleware',    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL
ROOT_URLCONF = 'tuition_project.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required by allauth
                'django.contrib.auth.context_processors.auth',
                'Notification.context_processors.user_notifications',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Site ID (required by allauth)
SITE_ID = 1

# Authentication Backends (for allauth + default)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Static & Media
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
hostname = socket.gethostname()
if 'pythonanywhere' in hostname:
    STATIC_ROOT = '/home/sajidiqbal/tutionwebsite/tuition_porject/static/'
    MEDIA_ROOT = '/home/sajidiqbal/tutionwebsite/tuition_porject/media/'
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        },
    }
}

# Login redirects
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# Allauth account settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
SOCIALACCOUNT_AUTO_SIGNUP = True  # Google login ke baad signup form skip kare
ACCOUNT_EMAIL_VERIFICATION = "none"  # Email verification skip, ya "optional" agar chaho

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True

# Default PK field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
