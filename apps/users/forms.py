from django import forms
from django.core import validators
from django_redis import get_redis_connection

from .models import MyUser
from utils.formserrors import FormsMixin

from verification import constants


class LoginForm(forms.Form, FormsMixin):
    password = forms.CharField(max_length=16, min_length=6, error_messages={
        'required': '请输入密码',
        'max_length': '密码格式不正确',
        'min_length': '密码格式不正确'
    })
    mobile = forms.CharField(max_length=11, min_length=11,
                             validators=[validators.RegexValidator(r'1[345789]\d{9}', message='手机格式不正确')],
                             error_messages={
                                 'required': '请输入账号',
                                 'max_length': '请输入正确格式的手机号',
                                 'min_length': '请输入正确格式的手机号'
                             }
                             )
    remember = forms.BooleanField(required=False)


class RegisterForm(forms.Form, FormsMixin):
    username = forms.CharField(max_length=100, required=True)
    mobile = forms.CharField(max_length=11, min_length=11,
                             validators=[validators.RegexValidator(r'1[345789]\d{9}', message="手机格式不正确")], )
    password = forms.CharField(min_length=6, max_length=16)
    password_repeat = forms.CharField(min_length=6, max_length=16)
    sms_code = forms.CharField(max_length=constants.SMS_LENGTH, min_length=constants.SMS_LENGTH)

    def clean(self):
        # 1，获取验证通过的数据
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        mobile = cleaned_data.get('mobile')
        # 2，验证密码是否一至
        if password != password_repeat:
            raise forms.ValidationError('密码输入不一致！')
        # 3，验证用户名是否重复
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已被注册！')
        # 4，验证手机号是否存在
        if MyUser.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError('手机号已被注册')
        # 5，验证短信验证码是否正确
        sms_captcha = cleaned_data.get("sms_code")
        # 5.1获取数据库连接
        try:
            redis_con = get_redis_connection(alias='verification')  # 连接数据库
        except:
            return forms.ValidationError('未知错误')
        # 5.2获取数据库手机验证码
        sms_key = "sms_{}".format(mobile)
        # 校检验证码是否为空（None）

        redis_sms_code = redis_con.get(sms_key).decode('utf-8') if redis_con.get(sms_key) else None

        # 5.3,判断短信验证码是否正确
        if sms_captcha != redis_sms_code:
            raise forms.ValidationError('手机验证码不正确')
        # 返回验证完的数据
        return cleaned_data
