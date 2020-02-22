from django import forms
from django.core import validators
from users.models import MyUser
from django_redis import get_redis_connection
from utils.formserrors import FormsMixin
class smsCodeForms(forms.Form,FormsMixin):
    mobile = forms.CharField(max_length=11,min_length=11,
                             validators=[
                                 validators.RegexValidator(r'1[3-9]\d{9}','手机号码格式不正确')
                             ],error_messages={
                                'max_length': '最大长度必能超过11',
                                'min_length': '最小长度不能小于11',
                                'required': '手机号码不能为空'
                            })
    image_code_id = forms.UUIDField(error_messages={
        'required': 'uuid不能为空'
    })
    text = forms.CharField(max_length=4,min_length=4,error_messages={
        'max_length': '最大长度为4',
        'min_length': '最小长度为4',
        'required': '验证码不能为空'
    })

    def clean(self):
        clean_data = super(smsCodeForms, self).clean()
        mobile_ = clean_data.get('mobile')
        image_code_id_ = clean_data.get("image_code_id")
        text_ = clean_data.get('text')
        try:
            redis_con = get_redis_connection(alias='verification')  # 连接数据库
        except:
            return forms.ValidationError('未知错误')
        img_key = 'img_{}'.format(image_code_id_)
        text =redis_con.get(img_key).decode('utf-8') if redis_con.get(img_key) else None
        #删除图片验证码
        redis_con.delete(img_key)
        # 判断短信验证码是否有发送记录
        sms_flag = redis_con.get('sms_flag_{}'.format(mobile_))
        if sms_flag:
            raise forms.ValidationError('获取验证码过于频繁')
        if not text:
            raise forms.ValidationError('验证码已失效')
        if text != text_.upper():
            raise forms.ValidationError('验证码错误')
        if MyUser.objects.filter(mobile=mobile_).count():
            raise forms.ValidationError('手机已被注册')
        return clean_data

