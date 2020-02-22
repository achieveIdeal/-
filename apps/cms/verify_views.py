from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import ContentType, Permission
from django.views import View
from rest_framework.settings import api_settings

from utils.resful import ToJsonData
from django.http.response import Http404
from django_redis import get_redis_connection
import time
from pprint import pprint


class VerifyView(LoginRequiredMixin, PermissionRequiredMixin, View):
    '''用户认证，权限认证，节流控制'''
    permission_required = []  # 模型所包含的权限，会自动获取
    model = None  # 指定模型，需手动指定，用于获取模型的权限
    SECOND = 10  # 秒
    FREQUENCY = 8  # 访问评率

    def get_ident(self, request):
        '''获取唯一标识，远程地址'''
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = request.META.get('REMOTE_ADDR')
        num_proxies = api_settings.NUM_PROXIES

        if num_proxies is not None:
            if num_proxies == 0 or xff is None:
                return remote_addr
            addrs = xff.split(',')
            client_addr = addrs[-min(num_proxies, len(addrs))]
            return client_addr.strip()

        return ''.join(xff.split()) if xff else remote_addr

    def throttle(self, request):
        '''节流限制'''
        conn = get_redis_connection(alias='throttle')
        remote_addr = self.get_ident(request)
        ctime = time.time()
        VISIT_REMOTE = conn.keys()
        # 判断该IP是否有过访问记录，没有就添加
        if remote_addr not in VISIT_REMOTE:
            conn.lpush(remote_addr, 0)
        # 有就获取他的访问记录
        history = conn.lrange(remote_addr, 0, -1)
        history = [float(t) for t in history]
        # 判断访问记录是否在10秒内到达了三次
        while history and ctime - history[-1] > float(self.SECOND):
            conn.rpop(remote_addr)
            # 重新获取值，下次遍历
            history = [float(t) for t in conn.lrange(remote_addr, 0, -1)]
        #     # 小于三次就可以继续访问
        if len(history) < self.FREQUENCY:
            history.insert(0, ctime)
            conn.lpush(remote_addr, ctime)
            return True

    def dispatch(self, request, *args, **kwargs):
        '''可将增删改查写为两个path，不用考虑因方法而报错'''
        if not self.throttle(request):  # 节流限制
            raise Http404('操作太频繁')
        if not self.checking_road(request):
            raise Http404('非法操作')
        else:
            return super(VerifyView, self).dispatch(request, *args, **kwargs)

    def checking_road(self, request):
        id = request.path.split('/')[-2]
        if request.method == "DELETE" or request.method == "PUT":
            try:
                int(id)
            except:
                return None

        if request.method == "GET" or  request.method == "POST":
            try:
                int(id)
                return None
            except:
                return True
        return True

    def get_permission_required(self):
        '''获取权限'''
        if not self.model:
            raise ValueError('未指定模型')
        code = ContentType.objects.get_for_model(self.model)
        perm = Permission.objects.filter(content_type=code).only('codename')
        for query in perm:
            codename = 'tag' + '.' + query.codename
            self.permission_required.append(codename)
        return self.permission_required

    def handle_no_permission(self):
        if self.raise_exception:
            return ToJsonData().unauth('没有权限访问')
        else:
            return super(VerifyView, self).handle_no_permission()

#################################测试代码######################################
# import time
# import redis

# from django_redis import get_redis_connection
# def throttle(request):
#     conn = redis.StrictRedis(db=3,decode_responses=True)
#     remote_addr = request
#     ctime = time.time()
#     VISIT_REMOTE = conn.keys()
#     # 判断该IP是否有过访问记录，没有就添加
#     if remote_addr not in VISIT_REMOTE:
#         conn.lpush(remote_addr,0)
#     # 有就获取他的访问记录
#     history = conn.lrange(remote_addr,0,-1)
#     history = [float(t) for t in history]
#     # 判断访问记录是否在10秒内到达了三次
#     while history and ctime - history[-1] > float(10):
#         conn.rpop(remote_addr)
#         #重新获取值，下次遍历
#         history = [float(t) for t in conn.lrange(remote_addr,0,-1)]
#     #     # 小于三次就可以继续访问
#     if len(history) < 3:
#         history.insert(0, ctime)
#         conn.lpush(remote_addr,ctime)
#         return True


#
# conn = redis.StrictRedis(db=3,decode_responses=True)
#
# conn.lpush('name','val')
# conn.lpush('name','val1')
# print(conn.lrange('name',0,-1))
# conn.keys()
