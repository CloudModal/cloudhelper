"""
Django settings for iam project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import ldap
from . import const
from .conf import load_user_config
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)


CONFIG = load_user_config()
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'iam.log')
GUNICORN_LOG_FILE = os.path.join(LOG_DIR, 'gunicorn.log')
VERSION = const.VERSION

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.DEBUG

# Absolute url for some case, for example email link
SITE_URL = CONFIG.SITE_URL

# LOG LEVEL
LOG_LEVEL = CONFIG.LOG_LEVEL

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'organization.apps.OrgConfig',
    'account.apps.AccountConfig',
    'access.apps.AccessConfig',
    'assets.apps.AssetsConfig',
    'authentication.apps.AuthenticationConfig',  # authentication
    'tickets.apps.TicketsConfig',
    'audits.apps.AuditsConfig',
    'ops.apps.OpsConfig',
    'common.apps.CommonConfig',

    'rest_framework',
    # 'drf_yasg',
    'captcha',
    'django_filters',
    'corsheaders',
    'bootstrap4',
    'django_celery_beat',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'authentication.backends.openid.middleware.OpenIDAuthenticationMiddleware',
    'iam.middleware.RequestMiddleware',
    'organization.middleware.OrgMiddleware',
]

ROOT_URLCONF = 'iam.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'iam.context_processor.iam_processor',
                'access.context_processor.access_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'iam.wsgi.application'


LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGIN_URL = reverse_lazy('authentication:login')

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DB_OPTIONS = {}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(CONFIG.DB_ENGINE.lower()),
        'NAME': CONFIG.DB_NAME,
        'HOST': CONFIG.DB_HOST,
        'PORT': CONFIG.DB_PORT,
        'USER': CONFIG.DB_USER,
        'PASSWORD': CONFIG.DB_PASSWORD,
        'ATOMIC_REQUESTS': True,
        'OPTIONS': DB_OPTIONS
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Logging setting
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'main': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(module)s %(levelname)s] %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'syslog': {
            'format': 'l2c: %(message)s'
        },
        'msg': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        # 将级别高于 INFO 的日志输出到控制台
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'main'
        },
        'file': {
            'encoding': 'utf8',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*100,
            'backupCount': 7,
            'formatter': 'main',
            'filename': LOG_FILE,
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.NullHandler',
            'formatter': 'syslog'
        },
        # 将级别高于 ERROR 的日志消息作为邮件发送给Admin
        'mail_admins': {
            'level': 'ERROR',
            'include_html': False,
            # 'formatter': 'standard',
            # 'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': LOG_LEVEL,
        },
        'django.request': {
            'handlers': ['console', 'file', 'syslog', 'mail_admins'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file', 'syslog', 'mail_admins'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django_auth_ldap': {
            'handlers': ['console', 'file'],
            'level': "INFO",
        },
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}

SYSLOG_ENABLE = False

if CONFIG.SYSLOG_ADDR != '' and len(CONFIG.SYSLOG_ADDR.split(':')) == 2:
    host, port = CONFIG.SYSLOG_ADDR.split(':')
    SYSLOG_ENABLE = True
    LOGGING['handlers']['syslog'].update({
        'class': 'logging.handlers.SysLogHandler',
        'facility': CONFIG.SYSLOG_FACILITY,
        'address': (host, int(port)),
    })

# I18N translation
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '{}/static/'.format(CONFIG.FORCE_SCRIPT_NAME)
STATIC_ROOT = os.path.join(PROJECT_DIR, "data", "static")
STATIC_DIR = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Media files (File, ImageField) will be save these

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'data', 'media').replace('\\', '/') + '/'

# Use django-bootstrap-form to format template, input max width arg
BOOTSTRAP_COLUMN_COUNT = 11

# Init data or generate fake data source for development
FIXTURE_DIRS = [os.path.join(BASE_DIR, 'fixtures'), ]

"""
If you want to force the use of a SES configuration set you can set the option below. 
This is useful when you want to do more detailed tracking of your emails such as opens and clicks. 
You can see more details at:
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/using-configuration-sets.html
"""
AWS_SES_CONFIGURATION_SET_NAME = CONFIG.AWS_SES_CONFIGURATION_SET_NAME

# Email config
# EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'
# EMAIL_HOST = 'smtp.l2c.org'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'noreply@l2c.org'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_FROM = 'dev@light2cloud.com'
# EMAIL_RECIPIENT = ''
# EMAIL_USE_SSL = False
# EMAIL_USE_TLS = False
# EMAIL_SUBJECT_PREFIX = '[L2C] '

# Email custom content
EMAIL_CUSTOM_USER_CREATED_SUBJECT = '用户创建成功'
EMAIL_CUSTOM_USER_CREATED_HONORIFIC = 'Dear'
EMAIL_CUSTOM_USER_CREATED_BODY = ''
EMAIL_CUSTOM_USER_CREATED_SIGNATURE = 'CloudHelper'

REST_FRAMEWORK = {
    # 自定义错误
    'EXCEPTION_HANDLER': 'common.utils.custom_execption.custom_exception_handler',
    # 对接口访问的频次进行限制，以减轻服务器压力
    'DEFAULT_THROTTLE_CLASSES': (
        # 登录用户节流
        # 'rest_framework.throttling.UserRateThrottle'
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        # 登录用户对应 的节流次数
        # 'user': '3/minute',
        'send_sms': '1/minute',
        'send_ses': '1/minute',
    },
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'common.permissions.IsOrgAdmin',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'common.renders.JMSCSVRender',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'common.parsers.JMSCSVParser',
        'rest_framework.parsers.FileUploadParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.backends.api.AccessKeyAuthentication',
        'authentication.backends.api.AccessTokenAuthentication',
        'authentication.backends.api.PrivateTokenAuthentication',
        'authentication.backends.api.SignatureAuthentication',
        'authentication.backends.api.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_METADATA_CLASS': 'common.drfmetadata.SimpleMetadataWithFilters',
    'ORDERING_PARAM': "order",
    'SEARCH_PARAM': "search",
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S %z',
    'DATETIME_INPUT_FORMATS': ['iso-8601', '%Y-%m-%d %H:%M:%S %z'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 15
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'authentication.backends.pubkey.PublicKeyAuthBackend',
    'authentication.backends.auth.EmailAuthenticationBackend',
    'authentication.backends.auth.MobileAuthenticationBackend'
]

# Custom User Auth model
AUTH_USER_MODEL = 'account.User'

# OTP settings
OTP_ISSUER_NAME = CONFIG.OTP_ISSUER_NAME
OTP_VALID_WINDOW = CONFIG.OTP_VALID_WINDOW

# Auth LDAP settings
AUTH_LDAP = False
AUTH_LDAP_SEARCH_PAGED_SIZE = CONFIG.AUTH_LDAP_SEARCH_PAGED_SIZE
AUTH_LDAP_SYNC_IS_PERIODIC = CONFIG.AUTH_LDAP_SYNC_IS_PERIODIC
AUTH_LDAP_SYNC_INTERVAL = CONFIG.AUTH_LDAP_SYNC_INTERVAL
AUTH_LDAP_SYNC_CRONTAB = CONFIG.AUTH_LDAP_SYNC_CRONTAB
AUTH_LDAP_USER_LOGIN_ONLY_IN_USERS = CONFIG.AUTH_LDAP_USER_LOGIN_ONLY_IN_USERS

AUTH_LDAP_SERVER_URI = 'ldap://localhost:389'
AUTH_LDAP_BIND_DN = 'cn=admin,dc=l2c,dc=org'
AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_SEARCH_OU = 'ou=tech,dc=l2c,dc=org'
AUTH_LDAP_SEARCH_FILTER = '(cn=%(user)s)'
AUTH_LDAP_START_TLS = False
AUTH_LDAP_USER_ATTR_MAP = {"username": "cn", "name": "sn", "email": "mail"}
AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER,
    ldap.OPT_REFERRALS: CONFIG.AUTH_LDAP_OPTIONS_OPT_REFERRALS
}
LDAP_CERT_FILE = os.path.join(PROJECT_DIR, "data", "certs", "ldap_ca.pem")
if os.path.isfile(LDAP_CERT_FILE):
    AUTH_LDAP_GLOBAL_OPTIONS[ldap.OPT_X_TLS_CACERTFILE] = LDAP_CERT_FILE
# AUTH_LDAP_GROUP_SEARCH_OU = CONFIG.AUTH_LDAP_GROUP_SEARCH_OU
# AUTH_LDAP_GROUP_SEARCH_FILTER = CONFIG.AUTH_LDAP_GROUP_SEARCH_FILTER
# AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
#    AUTH_LDAP_GROUP_SEARCH_OU, ldap.SCOPE_SUBTREE, AUTH_LDAP_GROUP_SEARCH_FILTER
# )
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_TIMEOUT: 30
}
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 1
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_BACKEND = 'authentication.backends.ldap.LDAPAuthorizationBackend'

if AUTH_LDAP:
    AUTHENTICATION_BACKENDS.insert(0, AUTH_LDAP_BACKEND)

# openid
# Auth OpenID settings
BASE_SITE_URL = CONFIG.BASE_SITE_URL
AUTH_OPENID = CONFIG.AUTH_OPENID
AUTH_OPENID_SERVER_URL = CONFIG.AUTH_OPENID_SERVER_URL
AUTH_OPENID_REALM_NAME = CONFIG.AUTH_OPENID_REALM_NAME
AUTH_OPENID_CLIENT_ID = CONFIG.AUTH_OPENID_CLIENT_ID
AUTH_OPENID_CLIENT_SECRET = CONFIG.AUTH_OPENID_CLIENT_SECRET
AUTH_OPENID_IGNORE_SSL_VERIFICATION = CONFIG.AUTH_OPENID_IGNORE_SSL_VERIFICATION
AUTH_OPENID_SHARE_SESSION = CONFIG.AUTH_OPENID_SHARE_SESSION
AUTH_OPENID_BACKENDS = [
    'authentication.backends.openid.backends.OpenIDAuthorizationPasswordBackend',
    'authentication.backends.openid.backends.OpenIDAuthorizationCodeBackend',
]

if AUTH_OPENID:
    LOGIN_URL = reverse_lazy("authentication:openid:openid-login")
    LOGIN_COMPLETE_URL = reverse_lazy("authentication:openid:openid-login-complete")
    AUTHENTICATION_BACKENDS.insert(0, AUTH_OPENID_BACKENDS[0])
    AUTHENTICATION_BACKENDS.insert(0, AUTH_OPENID_BACKENDS[1])

# Radius Auth
AUTH_RADIUS = CONFIG.AUTH_RADIUS
AUTH_RADIUS_BACKEND = 'authentication.backends.radius.RadiusBackend'
RADIUS_SERVER = CONFIG.RADIUS_SERVER
RADIUS_PORT = CONFIG.RADIUS_PORT
RADIUS_SECRET = CONFIG.RADIUS_SECRET

if AUTH_RADIUS:
    AUTHENTICATION_BACKENDS.insert(0, AUTH_RADIUS_BACKEND)

# Dump all celery log to here
CELERY_LOG_DIR = os.path.join(PROJECT_DIR, 'data', 'celery')

# Celery using redis as broker
CELERY_BROKER_URL = 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
    'password': CONFIG.REDIS_PASSWORD,
    'host': CONFIG.REDIS_HOST,
    'port': CONFIG.REDIS_PORT,
    'db': CONFIG.REDIS_DB_CELERY,
}
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_RESULT_EXPIRES = 3600
# CELERY_WORKER_LOG_FORMAT = '%(asctime)s [%(module)s %(levelname)s] %(message)s'
# CELERY_WORKER_LOG_FORMAT = '%(message)s'
# CELERY_WORKER_TASK_LOG_FORMAT = '%(task_id)s %(task_name)s %(message)s'
CELERY_WORKER_TASK_LOG_FORMAT = '%(message)s'
# CELERY_WORKER_LOG_FORMAT = '%(asctime)s [%(module)s %(levelname)s] %(message)s'
CELERY_WORKER_LOG_FORMAT = '%(message)s'
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_WORKER_REDIRECT_STDOUTS = True
CELERY_WORKER_REDIRECT_STDOUTS_LEVEL = "INFO"
# CELERY_WORKER_HIJACK_ROOT_LOGGER = True
# CELERY_WORKER_MAX_TASKS_PER_CHILD = 40
CELERY_TASK_SOFT_TIME_LIMIT = 3600

# Cache use redis
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
            'password': CONFIG.REDIS_PASSWORD,
            'host': CONFIG.REDIS_HOST,
            'port': CONFIG.REDIS_PORT,
            'db': CONFIG.REDIS_DB_CACHE,
        }
    }
}


# Captcha settings, more see https://django-simple-captcha.readthedocs.io/en/latest/advanced.html
CAPTCHA_IMAGE_SIZE = (80, 33)
CAPTCHA_FOREGROUND_COLOR = '#001100'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots', 'captcha.helpers.noise_arcs')
CAPTCHA_TEST_MODE = CONFIG.CAPTCHA_TEST_MODE
CAPTCHA_FIELD_TEMPLATE = 'captcha/text_field.html'
CAPTCHA_IMAGE_TEMPLATE = 'captcha/image.html'
CAPTCHA_HIDDEN_FIELD_TEMPLATE = 'captcha/hidden_field.html'
CAPTCHA_OUTPUT_FORMAT = '%(image)s %(hidden_field)s %(text_field)s'

COMMAND_STORAGE = {
    'ENGINE': 'terminal.backends.command.db',
}

DEFAULT_TERMINAL_COMMAND_STORAGE = {
    "default": {
        "TYPE": "server",
    },
}

TERMINAL_COMMAND_STORAGE = CONFIG.TERMINAL_COMMAND_STORAGE

DEFAULT_TERMINAL_REPLAY_STORAGE = {
    "default": {
        "TYPE": "server",
    },
}

TERMINAL_REPLAY_STORAGE = {
}


SECURITY_MFA_AUTH = False
SECURITY_COMMAND_EXECUTION = True
SECURITY_LOGIN_LIMIT_COUNT = 7
SECURITY_LOGIN_LIMIT_TIME = 30  # Unit: minute
SECURITY_MAX_IDLE_TIME = 30  # Unit: minute
SECURITY_PASSWORD_EXPIRATION_TIME = 9999  # Unit: day
SECURITY_PASSWORD_MIN_LENGTH = 6  # Unit: bit
SECURITY_PASSWORD_UPPER_CASE = False
SECURITY_PASSWORD_LOWER_CASE = False
SECURITY_PASSWORD_NUMBER = False
SECURITY_PASSWORD_SPECIAL_CHAR = False
SECURITY_PASSWORD_RULES = [
    'SECURITY_PASSWORD_MIN_LENGTH',
    'SECURITY_PASSWORD_UPPER_CASE',
    'SECURITY_PASSWORD_LOWER_CASE',
    'SECURITY_PASSWORD_NUMBER',
    'SECURITY_PASSWORD_SPECIAL_CHAR'
]
SECURITY_MFA_VERIFY_TTL = CONFIG.SECURITY_MFA_VERIFY_TTL
SECURITY_SERVICE_ACCOUNT_REGISTRATION = CONFIG.SECURITY_SERVICE_ACCOUNT_REGISTRATION
TERMINAL_PASSWORD_AUTH = CONFIG.TERMINAL_PASSWORD_AUTH
TERMINAL_PUBLIC_KEY_AUTH = CONFIG.TERMINAL_PUBLIC_KEY_AUTH
TERMINAL_HEARTBEAT_INTERVAL = CONFIG.TERMINAL_HEARTBEAT_INTERVAL
TERMINAL_ASSET_LIST_SORT_BY = CONFIG.TERMINAL_ASSET_LIST_SORT_BY
TERMINAL_ASSET_LIST_PAGE_SIZE = CONFIG.TERMINAL_ASSET_LIST_PAGE_SIZE
TERMINAL_SESSION_KEEP_DURATION = CONFIG.TERMINAL_SESSION_KEEP_DURATION
TERMINAL_HOST_KEY = CONFIG.TERMINAL_HOST_KEY
TERMINAL_HEADER_TITLE = CONFIG.TERMINAL_HEADER_TITLE
TERMINAL_TELNET_REGEX = CONFIG.TERMINAL_TELNET_REGEX

TOKEN_EXPIRATION = CONFIG.TOKEN_EXPIRATION
DISPLAY_PER_PAGE = CONFIG.DISPLAY_PER_PAGE
DEFAULT_EXPIRED_YEARS = 70
USER_GUIDE_URL = ""


SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'iam.swagger.CustomSwaggerAutoSchema',
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}


# Default email suffix
EMAIL_SUFFIX = CONFIG.EMAIL_SUFFIX
LOGIN_LOG_KEEP_DAYS = CONFIG.LOGIN_LOG_KEEP_DAYS

# User or user group permission cache time, default 3600 seconds
ASSETS_PERM_CACHE_ENABLE = CONFIG.ASSETS_PERM_CACHE_ENABLE
ASSETS_PERM_CACHE_TIME = CONFIG.ASSETS_PERM_CACHE_TIME

# Asset user auth external backend, default AuthBook backend
BACKEND_ASSET_USER_AUTH_VAULT = False

DEFAULT_ORG_SHOW_ALL_USERS = CONFIG.DEFAULT_ORG_SHOW_ALL_USERS

PERM_SINGLE_ASSET_TO_UNGROUP_NODE = CONFIG.PERM_SINGLE_ASSET_TO_UNGROUP_NODE
WINDOWS_SSH_DEFAULT_SHELL = CONFIG.WINDOWS_SSH_DEFAULT_SHELL
FLOWER_URL = CONFIG.FLOWER_URL


# Django channels support websocket
CHANNEL_REDIS = "redis://:{}@{}:{}/{}".format(
    CONFIG.REDIS_PASSWORD, CONFIG.REDIS_HOST, CONFIG.REDIS_PORT,
    CONFIG.REDIS_DB_WS,
)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [CHANNEL_REDIS],
        },
    },
}

SES_EMAIL_SENDER = CONFIG.SES_EMAIL_SENDER
SES_EMAIL_SENDERNAME = CONFIG.SES_EMAIL_SENDERNAME
SES_EMAIL_USERNAME_SMTP = CONFIG.SES_EMAIL_USERNAME_SMTP
SES_EMAIL_PASSWORD_SMTP = CONFIG.SES_EMAIL_PASSWORD_SMTP
SES_EMAIL_HOST = CONFIG.SES_EMAIL_HOST
SES_EMAIL_PORT = CONFIG.SES_EMAIL_PORT

# 阿里云短信服务
ALI_ACCESS_KEY_ID = CONFIG.ALI_ACCESS_KEY_ID
ALI_ACCESS_KEY_SECRET = CONFIG.ALI_ACCESS_KEY_SECRET
ALI_PRODUCT_NAME = CONFIG.ALI_PRODUCT_NAME
ALI_REGION = CONFIG.ALI_REGION
ALI_DOMAIN = CONFIG.ALI_DOMAIN
ALI_SIGN_NAME = CONFIG.ALI_SIGN_NAME
ALI_TEMPLATE_CODE = CONFIG.ALI_TEMPLATE_CODE

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie
CORS_ORIGIN_ALLOW_ALL = True  # 允许所有域名跨域(优先选择)
# 配置白名单
# CORS_ORIGIN_WHITELIST = (
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8080",
#     "http://localhost:8000",
#     "http://127.0.0.1:8000"
# )

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
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
    'x-requested-org',
    'XMLHttpRequest',
    'X_FILENAME',
)

ADMINS = (
    ('admin', 'admin@cloudhelper.xyz'),
)
# 凭证数量
CREDENTIALS_MOST = CONFIG.CREDENTIALS_MOST

# 跨账户设置
CHINA_ACCOUNT_ID = CONFIG.CHINA_ACCOUNT_ID
CHINA_REQUIRE_EXTERNAL_ID = CONFIG.CHINA_REQUIRE_EXTERNAL_ID
CHINA_EXTERNAL_ID = CONFIG.CHINA_EXTERNAL_ID
CHINA_REQUIRE_MFA = CONFIG.CHINA_REQUIRE_MFA
CHINA_AWS_ACCESS_KEY_ID = CONFIG.CHINA_AWS_ACCESS_KEY_ID
CHINA_AWS_SECRET_ACCESS_KEY = CONFIG.CHINA_AWS_SECRET_ACCESS_KEY

GLOBAL_ACCOUNT_ID = CONFIG.GLOBAL_ACCOUNT_ID
GLOBAL_REQUIRE_EXTERNAL_ID = CONFIG.GLOBAL_REQUIRE_EXTERNAL_ID
GLOBAL_EXTERNAL_ID = CONFIG.GLOBAL_EXTERNAL_ID
GLOBAL_REQUIRE_MFA = CONFIG.GLOBAL_REQUIRE_MFA
GLOBAL_AWS_ACCESS_KEY_ID = CONFIG.GLOBAL_AWS_ACCESS_KEY_ID
GLOBAL_AWS_SECRET_ACCESS_KEY = CONFIG.GLOBAL_AWS_SECRET_ACCESS_KEY

ROLE_SESSION_NAME = CONFIG.ROLE_SESSION_NAME

# 默认跨域不允许携带cookie
# https://docs.djangoproject.com/en/2.2/ref/settings/#session-cookie-samesite
SESSION_COOKIE_SAMESITE = None


# 日志系统的url, api记录日志使用
LOG_CORE_HOST = CONFIG.LOG_CORE_HOST

# 写入日志验证身份
IAM_URL = CONFIG.IAM_URL
IAM_ACCESS_KEY_ID = CONFIG.IAM_ACCESS_KEY_ID
IAM_SECRET_ACCESS_KEY = CONFIG.IAM_SECRET_ACCESS_KEY

RECEIVE_ERROR_MAIL = CONFIG.RECEIVE_ERROR_MAIL
RECEIVE_ERROR_MAIL_NAME = CONFIG.RECEIVE_ERROR_MAIL_NAME

# Amazon SQS 消息队列
AWS_ACCESS_KEY_ID = CONFIG.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = CONFIG.AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION = CONFIG.AWS_DEFAULT_REGION
INSPECT_SQS_QUEUE_URL = CONFIG.INSPECT_SQS_QUEUE_URL
