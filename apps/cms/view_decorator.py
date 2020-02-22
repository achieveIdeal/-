from functools import  wraps
from django.shortcuts import redirect,reverse
#装饰器，判断是否是超级用户，不是则回到主页
def has_permission(url,perms=None):
    def wrapper(func):
        @wraps(func)
        def verify_perms(request,*args,**kwargs):
            if request.user.is_superuser:

                return  func(request,*args,**kwargs)
            elif perms and request.user.has_perm(perms):


                return func(request,*args,**kwargs)
            else:
                return redirect(reverse(url))
        return verify_perms
    return wrapper

