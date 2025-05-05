import os
from pathlib import Path
import socket

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Installed applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'Home',
    'users',
    'courses',
    'Tutor',
    'student',
    'payments',  # Course management apps
    'live_classes',
    'assignments',
    'contact',
    'crispy_forms',
    'crispy_bootstrap5',  # For Bootstrap 5 compatibility
]

# Crispy Forms settings
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Middleware settings
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # This line for serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'tuition_porject.urls'

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],  # Templates directory
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

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Security settings
SECRET_KEY = 'django-insecure-gsutf%$^_2g(*!2@6dj-@rn_z2_sj)e!5#@-4w#muq#u+2r#eq'

DEBUG = True

ALLOWED_HOSTS = [
    'sajidiqbal.pythonanywhere.com',  # Production domain
    'localhost',  # Localhost for development
    '127.0.0.1',  # Localhost IP
]



# Define the URL path for serving static files
import os
from pathlib import Path
import socket

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Static URL
STATIC_URL = '/static/'

# Define static and media file paths for local and production environments
hostname = socket.gethostname()

if 'pythonanywhere' in hostname:
    # For PythonAnywhere (production)
    STATIC_ROOT = '/home/sajidiqbal/tuition_project/static/'
    MEDIA_ROOT = '/home/sajidiqbal/tuition_project/media/'
else:
    # For local development
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Add this line to define STATIC_ROOT

# For production (using WhiteNoise)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Collect static files to the STATIC_ROOT directory






# Database configuration (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,  # Retry the connection for 20 seconds
        },
    }
}

# Authentication settings
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'  # Set this according to your local timezone
USE_I18N = True
USE_TZ = True

# Default auto field setting
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings (optional, uncomment if you need email configuration)
# ADMIN_EMAIL = 'sajidiqbal.bk.8888@gmail.com'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# DEFAULT_FROM_EMAIL = 'noreply@tuition.com'
