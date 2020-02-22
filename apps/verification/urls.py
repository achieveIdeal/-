from django.urls import path, re_path
from . import views

app_name = 'verification'

urlpatterns = [
    path('image_codes/<uuid:uuid>/', views.image_code, name='code'),
    path('sms_code/', views.smsCode.as_view(), name='sms_code'),
    re_path('username/(?P<username>[a-zA-Z0-9]{5,20})/', views.verify_username, name='username'),
    re_path('mobiles/(?P<mobile>1[3-9]\d{9})/', views.verify_mobile, name='mobile')
]
