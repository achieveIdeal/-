from django_redis import get_redis_connection

from utils.aliyunsms.aliyunsms import send_sms
import json
import logging

from celery_tasks.celery_sms import app
from utils.resful import ToJsonData
from verification import constants

logger = logging.getLogger('django')

# celery -A celery_tasks.celery_sms worker -l info
#-A 指定创建app应用文件
# worker 指定进程数，默认为电脑cpu核数
#-l 日志信息登记
@app.task(name='send_sms_code') #创建异步任务
def send_sms_code(mobile, code):
    '''异步任务不需要返回值'''
    res = send_sms(mobile, code=code).decode()
    result = json.loads(res)
    if result['Message'].lower() != 'ok':
        logger.error('{}短信验证码超额'.format(mobile))
    else:
        logger.info('短信发送成功！')

