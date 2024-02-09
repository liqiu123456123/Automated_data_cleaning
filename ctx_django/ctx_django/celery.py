import os
from celery import Celery
# 获取settings.py的配置信息
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctx_django.settings')
# 定义Celery对象，并将项目配置信息加载到对象中。
# Celery的参数一般以项目名称命名
app = Celery('ctx_django')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()