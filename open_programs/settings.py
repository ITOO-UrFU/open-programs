import os
import sys
import platform
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from configurations import Configuration


class Common(Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # SECURITY WARNING: don't run with debug turned on in production!
    SECRET_KEY = '&p(zt!@%h#+f+i%@avy9=v5bfi!pz(0rv@-6w%(#olfe(@b^i0'

    ALLOWED_HOSTS = ['*', ]

    PROJECT_ROOT = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django_extensions',
        'reversion',
        'rosetta',
        'dashing',  # Read https://github.com/talpor/django-dashing/
        'djcelery_email',
        'admin_reorder',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.vk',
        'allauth.socialaccount.providers.instagram',
        'allauth.socialaccount.providers.odnoklassniki',
        'allauth.socialaccount.providers.openid',
        'allauth.socialaccount.providers.twitter',
        'courses',
        'directories',
        'journal',
        'persons',
        'professions',
        'programs',
        'modules',
        'discipline',
        'base',
    ]

    if platform.system() not in ('Windows', 'Darwin'):
        INSTALLED_APPS.append('haystack')

    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'admin_reorder.middleware.ModelAdminReorder',
    ]

    ROOT_URLCONF = 'open_programs.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, "templates")],
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

    WSGI_APPLICATION = 'open_programs.wsgi.application'

    SITE_ID = 1

    # Database
    # https://docs.djangoproject.com/en/1.9/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
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
    # https://docs.djangoproject.com/en/1.9/topics/i18n/
    LANGUAGE_CODE = 'ru'

    TIME_ZONE = 'Asia/Yekaterinburg'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    #### STATIC ####
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]

    #### SOCIAL ####

    SOCIALACCOUNT_QUERY_EMAIL = True

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    )

    #### HAYSTACK ####

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
        'elasticsearch': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }

    #### LOCALES ####

    LOCALE_PATHS = (
        BASE_DIR + '/locale', )

    LANGUAGES = [
        ('ru', _('Russian')),
        ('en', _('English')),
    ]

    #### MEDIA ####

    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"

    #### EMAIL ####
    EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

    CELERY_EMAIL_TASK_CONFIG = {
        'name': 'djcelery_email_send',
        'ignore_result': True,
        'queue': 'email',
        'rate_limit': '50/m',
    }

    LOGIN_REDIRECT_URL = "/"

    #### ADMIN REORDER ####
    ADMIN_REORDER = (
        {'app': 'programs', 'label': 'Открытые образовательные программы'},
        {'app': 'modules', 'label': 'Типы модулей', 'models': ('modules.Type', )},
        {'app': 'modules', 'label': 'Модули', 'models': ('modules.Module', )},
        {'app': 'modules', 'label': 'Контейнеры модулей', 'models': ('modules.GeneralBaseModulesPool',
                                                                     'modules.EducationalProgramTrajectoriesPool',
                                                                     'modules.ChoiceModulesPool')},
        {'app': 'auth', 'label': 'Пользователи', 'models': ('auth.User', )},
        {'app': 'persons', 'label': 'Персоны'},
        {'app': 'courses', 'label': 'Курсы и запуски курсов'},
        {'app': 'directories', 'label': 'Справочники'},
        {'app': 'disciplines', 'label': 'Дисциплины'},
        {'app': 'journal', 'label': 'Электронный дневник'},
        {'app': 'professions', 'label': 'Профессии'},
    )

#### REWRITE ADMIN TITLES ####
    admin.site.site_header = _('Открытые образовательные программы')
    admin.site.site_title = _('Администрирование')
    admin.site.index_title = _('Открытые образовательные программы')


class Dev(Common):

    DEBUG = True
    SECRET_KEY = '&p(zt!@%h#+f+i%@avy9=v5bfi!pz(0rv@-6w%(#olfe(@b^i0'


class Prod(Common):

    DEBUG = False
    #INSTALLED_APPS.append('django_mysql') # Read https://django-mysql.readthedocs.io/en/latest/installation.html
