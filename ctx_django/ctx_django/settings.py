import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'account.UserModel'

SECRET_KEY = 'django-insecure-znyce!f7jh1-4uu0d-l=&a$c6luasieh$m2mx)o#@1ugr8$^jm'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    "netdisk",
    'rest_framework',
    # 添加异步任务功能
    'django_celery_results',
    # 添加定时任务功能
    'django_celery_beat'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'ctx_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',  # 模板中可以使用{{ MEDIA_URL }}
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ctx_django.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# 语言和时区设置
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static')),

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 文件保存位置

SESSION_COOKIE_AGE = 24 * 60 * 60  # 登录有效时间-秒
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 关闭浏览器时登录失效

CACHE_PATH = os.path.join(BASE_DIR, 'media', 'cache')
IMAGE_CACHE_TYPE = '.jpg'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 发送邮件配置信息
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# smtp的服务器地址
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = '填入你的邮箱'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = '这里填入你的邮箱授权码'
# 收件人看到的发件人<>里面的内容必须和发送邮件的邮箱码一直
EMAIL_UES_TLS = '填入你的邮箱'


# 设置存储Celery任务队列的Redis数据库
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/4'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
# 设置存储Celery任务结果的数据库
CELERY_RESULT_BACKEND = 'django-db'

# 设置定时任务相关配置
CELERY_ENABLE_UTC = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'