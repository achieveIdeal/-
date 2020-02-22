from celery import Celery

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','djangoProjectClass.settings')

app = Celery('djangoProjectClass')  #创建celery应用

app.config_from_object('celery_tasks.celery_config') #配置文件中读取celery配置

#导入任务
app.autodiscover_tasks(['celery_tasks.sms',])