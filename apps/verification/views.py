import json
import string
import random

from django_redis import get_redis_connection
from django.http import HttpResponse, JsonResponse
from django.views import View

from users.models import MyUser
from . import constants
from .forms import *

from utils.captcha.captcha import captcha
from utils.resful import ToJsonData
from utils.aliyunsms.aliyunsms import send_sms

'''日志'''
import logging

logger = logging.getLogger('django')


# image_codes/<uuid:uuid>/
def image_code(request, uuid):
    ''' 定义获取图形验证视图'''
    # 1,获取redis数据库连接
    try:
        redis_connection = get_redis_connection(alias='verification')  # 连接数据库
    except:
        return ToJsonData().servererr(message='未知错误')
    # 2，获取前端传递的uuid
    img_key = 'img_{}'.format(uuid)
    # 3，生成验证图片和验证码
    text, img = captcha.generate_captcha()
    # 4，将图形验证码通过拼接uuid的方式储存之redis数据库
    redis_connection.setex(img_key,
                           constants.IMG_CODE_EXPIRY, text)  # 键，过期时间，值，
    # 5，打印logger日志
    logger.info('Img_code:{}'.format(text))
    # 6，返回图形验证码
    return HttpResponse(content=img,
                        content_type='image/jpg')  # 返回一张图片，可在模板中{% url 'verification:code' %}加载


# username/(?P<username>[a-zA-Z0-9]{5,20})/
def verify_username(request, username):
    '''验证用户名是否已存在'''
    if request.method == 'GET':
        # 1，获取传入的用户名，通过数据库查询判断是否已存在
        count = MyUser.objects.filter(username=username).count()
        # 2，构造返回数据
        data = {
            'count': count,
            'username': username
        }
        # 3，返回数据
        return JsonResponse({'data': data})


# mobiles/(?P<mobile>1[3-9]\d{9})/
def verify_mobile(request, mobile):
    '''验证手机号是否已存在'''
    if request.method == 'GET':
        count = MyUser.objects.filter(mobile=mobile).count()
        data = {
            'count': count,
            'mobile': mobile
        }
        return JsonResponse({'data': data})


# sms_code/
from celery_tasks.sms.tasks import send_sms_code  #异步发送短信
class smsCode(View):
    '''校检用户名图形验证码等，校检成功发送短信验证码'''

    def post(self, request):
        # 1，获取参数
        try:
            json_data = request.body.decode()
            data = json.loads(json_data)
        except Exception as e:
            logger.error('参数传递出现错误，json.loads无法解析')
            return ToJsonData().paramserr(message='参数错误')
        form = smsCodeForms(data=data)
        # 2，校检参数
        if form.is_valid():
            # 3，获取手机号码
            mobile = form.cleaned_data.get('mobile')
            # 4，产生随机验证码
            code = ''.join([random.choice(string.digits) for _ in range(constants.SMS_LENGTH)])  # 写算法随机
            # 5，获取redis数据库连接
            try:
                redis_con = get_redis_connection(alias='verification')  # 连接数据库
                logger.info('{}短信验证码发送成功'.format(mobile))
                # 7，将短信验证码存入数据库
                sms_key = 'sms_{}'.format(mobile)
                sms_flag_key = 'sms_flag_{}'.format(mobile)
                # 创建管道，执行多条写入命令
                pipe = redis_con.pipeline()
            except:
                logger.error('获取redis连接时出错')
                return ToJsonData().servererr(message='未知错误')  # 6，发送短信验证码
            '''开发阶段不用正式的短信，已测试成功可用'''
            # send_sms_code.delay(mobile,code) #调用异步任务，存入异步redis队列


            # res = send_sms(mobile, code=code).decode()
            # result = json.loads(res)
            # # 判断验证码是否发送成功
            # if result['Message'].lower() != 'ok':
            #     logger.error('{}短信验证码超额'.format(mobile))
            #     return ToJsonData().paramserr(message='验证码数量已超额')

            try:
                pipe.setex(sms_key, constants.SMS_CODE_EXPIRY, code)
                # 保存发送短信标记
                pipe.setex(sms_flag_key, constants.SMS_FLAG_EXPIRY, 1)
                # 执行管道内的命令
                pipe.execute()
                logger.info('验证码保存成功：{}'.format(code))
            except Exception as e:
                logger.debug('保存短信验证码时出现异常，{}'.format(e))
                return ToJsonData().servererr(message='服务器异常', data={})
            # 8,返回发送成功结果
            return ToJsonData().ok(message='发送成功', data={})
        else:
            errors = form.get_errors()
            return ToJsonData().paramserr(message=errors)
