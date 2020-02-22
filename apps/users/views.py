import json
import logging

from django.http import Http404, FileResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.views import View

from djangoProjectClass.settings import MEDIA_URL
from news.models import Document
from .models import MyUser
from .forms import LoginForm, RegisterForm
from utils.resful import ToJsonData

logger = logging.getLogger('django')


# login/
def login_view(request):
    '''登录视图'''
    if request.method == 'POST':
        # 1，获取数据
        forms = LoginForm(request.POST)
        # 2，验证数据
        if forms.is_valid():
            mobile = forms.cleaned_data.get('mobile')
            password = forms.cleaned_data.get('password')
            remember = forms.cleaned_data.get('remember')
            # 3，验证用户
            user = authenticate(request, username=mobile, password=password)
            # 4，验证用户是否存在
            if user:
                # 5，验证用户是否活跃
                if user.is_active:
                    # 6，登录，保存session
                    login(request, user)
                    # 7，是否记住该用户
                    if remember:
                        # 8，设置session过期时间
                        request.session.set_expiry(None)
                        # 9，返回登陆成功
                        return ToJsonData().ok(message='登录成功')
                    else:
                        request.session.set_expiry(0)
                        return ToJsonData().ok(message='登陆成功')
                else:
                    # 10，返回用户不活跃信息
                    return ToJsonData().unauth(message='该用户已被冻结', data={})
            else:
                # 11，返回校检用户失败信息
                return ToJsonData().paramserr(message='用户名或密码错误')
        else:
            error = forms.get_errors()
            print(error)
            return ToJsonData().paramserr(message=error, data={})
    # get请求返回登录页面
    if request.method == 'GET':
        return render(request, 'users/login.html')


# register/
def register(request):
    '''注册用户'''
    if request.method == 'GET':
        return render(request, 'users/register.html')

    if request.method == 'POST':
        try:
            json_data = request.body
            data = json.loads(json_data)
        except Exception as e:
            logger.error('参数传递出现错误，json.loads无法解析')
            return ToJsonData().paramserr(message='参数错误')
        forms = RegisterForm(data)
        if forms.is_valid():
            username = forms.cleaned_data.get('username')
            password = forms.cleaned_data.get('password')
            mobile = forms.cleaned_data.get('mobile')
            user = MyUser.objects.create_user(mobile=mobile, username=username, password=password)
            # 注册成功直接登陆
            login(request, user)
            return ToJsonData().ok('注册成功')
        else:
            error = forms.get_errors()
            return ToJsonData().paramserr(message=error)


def login_out(request):
    logout(request)
    return redirect(reverse('index'))


def download(request):
    '''下载文档页面'''
    docs = Document.objects.filter(is_delete=False).only('title','desc','author__username','image_url')

    return render(request, 'doc/docDownload.html',locals())

class DownLoadFile(View):
    '''文档下载'''
    def get(self,request,doc_id):
        #获取文档路径
        doc = Document.objects.filter(is_delete=False,pk=doc_id).only('file_url').first()

        if not doc:
            raise Http404('文件未找到')

        file_name = doc.file_url.split('/')[-1]
        import requests
        #生成url
        doc_url = request.build_absolute_uri(MEDIA_URL + file_name)
        try:
            #构造六响应
            # res = StreamingHttpResponse()
            #构造文件响应
            res = FileResponse(requests.get(doc_url,stream=True))
        except Exception as e:
            raise Http404('下载失败')
        ex_name = doc_url.split('.')[-1]

        if not ex_name:
            raise Http404('文件名异常')
        else:
            ex_name = ex_name.lower()

        if ex_name == 'pdf':
            res['Content-type'] = 'application/pdf'

        elif ex_name == 'doc':
            res['Content-type'] = 'application/msowrd'

        elif ex_name == 'ppt':
            res['Content-type'] = 'application/powerpoint'

        else:
            raise Http404('文件格式不正确')
        # res.streaming_content = requests.get(doc_url)
        #inline 是直接打开
        res['Content-Disposition'] = "attachment;filename*=UTF-8''{}".format(file_name)

        return res
