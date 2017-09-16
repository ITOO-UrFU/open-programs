import os
import platform
import sys
import datetime
from django.contrib import admin
from django.conf import settings

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = '&p(zt!@%h#+f+i%@avy9=v5bfi!pz(0rv@-6w%(#olfe(@b^i0'

ALLOWED_HOSTS = ['*', ]

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

DEBUG = True
# Application definition

INSTALLED_APPS = [
    'persons',
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
    'djcelery_email',
    'permission',
    'admin_reorder',
    'smuggler',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'codemirror2',
    'tinymce',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.odnoklassniki',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.twitter',
    'ajax_select',
    'courses',
    'directories',
    'journal',
    'professions',
    'programs',
    'modules',
    'disciplines',
    "competences",
    "results",
    "base",
    "constructor",
    "constructor_v2",
    "api",
    "api_v11",
    "uni",
    "cms",
    "stat",
]

if platform.system() not in ('Windows', 'Darwin', 'FreeBSD', 'Linux'):
    INSTALLED_APPS.append('haystack')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
    'reversion.middleware.RevisionMiddleware',
]

ROOT_URLCONF = 'open_programs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), os.path.join(BASE_DIR, "constructor")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
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
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'open_programs',
        'USER': 'root',
        'PASSWORD': 'ye;yj,jkmitrjlfmysql'
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
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

#### FIXTURES ####

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, "fixtures"),
]

#### SOCIAL ####

SOCIALACCOUNT_QUERY_EMAIL = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    "permission.backends.PermissionBackend",
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

LOGIN_REDIRECT_URL = "/constructor/"

#### ADMIN REORDER ####
ADMIN_REORDER = (
    {'app': 'cms', 'label': 'Управление контентом'},
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
    {'app': 'results', 'label': 'Результаты обучения'},
    {'app': 'competences', 'label': 'Компетенции'},
    {"app": "uni"},
)

#### REWRITE ADMIN TITLES ####
admin.site.site_header = _('Открытые образовательные программы')
admin.site.site_title = _('Открытые образовательные программы')
admin.site.index_title = _('Администрирование')

#### PERMISSION ####
PERMISSION_CHECK_TEMPLATES_OPTIONS_BUILTINS = False

#### SMUGGLER ####
SMUGGLER_FIXTURE_DIR = FIXTURE_DIRS[0]

#### CODEMIRROR ####
CODEMIRROR_PATH = os.path.join(STATICFILES_DIRS[0], "vendor", "codemirror")

#### REST FRAMEWORK ####
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': settings.SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3600),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,

}

NEED_ACTIVATE = False
REST_USE_JWT = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
DEFAULT_FROM_EMAIL = "no-reply@openedu.urfu.ru"



#### CORS ####
CORS_ORIGIN_WHITELIST = (
    # '192.168.0.100:4200',
    # 'localhost:4200',
    # '127.0.0.1:4200',
    # "http://openprograms.ru",
    # "openprograms.ru",
    # "http://openedu.urfu.ru",
    "openedu.urfu.ru",
)

CORS_URLS_REGEX = r'^/api/v11/.*$'

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)


JSON_EDITOR_JS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/5.5.11/jsoneditor.min.js'
JSON_EDITOR_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/5.5.11/jsoneditor.min.css'

AJAX_LOOKUP_CHANNELS = {
    'discipline': ('disciplines.lookups', 'DisciplineLookup'),
    'semester': ('disciplines.lookups', 'SemesterLookup'),
    'program': ('programs.lookups', 'ProgramLookup'),
    'module': ('modules.lookups', 'ModuleLookup'),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached',
        # 'LOCATION': '_cache',
    }
}
