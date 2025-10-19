import os
from decouple import config, Config, RepositoryEnv
from pathlib import Path
import pymysql
pymysql.install_as_MySQLdb()
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Decide which env file to load
DJANGO_ENV = os.environ.get("DJANGO_ENV", "dev")  # default to dev

if DJANGO_ENV == "prod":
    env_file = os.path.join(BASE_DIR, ".env.prod")
else:
    env_file = os.path.join(BASE_DIR, ".env.dev")

# Load env file
config = Config(RepositoryEnv(env_file))

#THis is for the api key for the gemini AI
AI_API_KEY = config("AI_API_KEY")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="").split(",")


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "register_page", #page
    "login_page", #page
    "landing_page", #page - at here there is the search page for job positing and candidate search.also include a page to apply for a job and send invitation to the applicant.
    "profile_user", #page
    "my_job_ad", #page - this one is more to the employer
    "my_job_list", #page - this one is more to the applicant
    "manage_applicant",#page
    "verify_applicant",#page
    "verification_request", #model
    "job_application", #model
    "application_user", #model
    "document", #model
    "education_vocation_training",#model
    "career_history",#model
    "skill", #model
    "communication_style", #model
    "personal_interest", #model
    "work_attitude", #model
    "job_ad", #model
]

AUTH_USER_MODEL = 'application_user.ApplicationUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Note: We keep whitenoise but Nginx handles file serving when DEBUG=False
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nasom_job_portal.urls'

# Base directory (Redefined, but this is okay)
BASE_DIR = Path(__file__).resolve().parent.parent

# Templates setup
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Project-level templates
        'APP_DIRS': True,  # Auto-find templates inside app folders
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

# Static files (CSS, JS, images) - These are the default DEV/relative settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')  # Global static folder
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


WSGI_APPLICATION = 'nasom_job_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Media files (User Uploads) - These are the default DEV/relative settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'

#Jazzmin setting bro
JAZZMIN_SETTINGS = {
    "site_title": "Autism Job Hiring Portal Admin",
    "site_header": "NASOM Admin",
    "site_brand": "NASOM Portal",
    "site_logo": "images/admin-logo.png",
    "welcome_sign": "Welcome to Job Hiring Portal for Autistic Individual",
    "copyright": "NASOM",
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "order_with_respect_to": ["auth", "jobs", "users"],
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")


# =========================================================
# PRODUCTION OVERRIDES (CRITICAL FOR DOCKER/NGINX)
# =========================================================

if DJANGO_ENV == "prod":
    # The paths must match the absolute volume mount points 
    # defined in the docker-compose.yml for the 'web' service 
    # and referenced by the 'nginx' service.

    # STATIC_ROOT: Where collectstatic puts the files
    STATIC_ROOT = '/vol/static'

    # MEDIA_ROOT: Where user uploads are saved
    MEDIA_ROOT = '/vol/media'

    # Ensure ALLOWED_HOSTS is securely configured in .env.prod
    # For Docker: Gunicorn should use a high-performance WSGI server 
    # and proxy headers (handled by Nginx).
