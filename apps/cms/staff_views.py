from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_POST

from users.models import MyUser
from django.contrib.auth.models import Permission,ContentType,Group
from django.views import  View

from utils.resful import ToJsonData
from .view_decorator import has_permission
from django.utils.decorators import method_decorator
@has_permission('cms:index')
def staff(request):
    staffs = MyUser.objects.select_related().filter(is_staff=True)
    context = {
        'staffs':staffs
    }
    return render(request,'cms/staff.html',context=context)

@method_decorator(has_permission('cms:index'),name='dispatch')
class AddStaff(View):
    def get(self,request):
        user_id = request.GET.get('user_id')
        groups = Group.objects.all().only('name')
        context = {
            'groups': groups
        }
        if not user_id:

            return render(request, 'cms/add_staff.html', context=context)
        else:
            user = MyUser.objects.filter(pk=user_id).only('mobile').first()
            mobile = user.mobile
            return render(request, 'cms/add_staff.html', locals())

    def post(self,request):
        mobile = request.POST.get('telephone')
        #获取多个同名的值
        groups_id = request.POST.getlist('groups')
        groups = Group.objects.filter(id__in=groups_id)
        try:
            user = MyUser.objects.get(mobile=mobile)
            user.is_staff = True
            user.save()
        except Exception as e:
            return ToJsonData().paramserr('添加失败')
        user.groups.set(groups)
        return redirect(reverse('cms:staff'))



@require_POST
def edit_staff(request):
    mobile = request.POST.get('telephone')
    # 获取多个同名的值
    groups_id = request.POST.getlist('groups')
    groups = Group.objects.filter(id__in=groups_id)
    try:
        user = MyUser.objects.get(mobile=mobile)
        user.is_staff = True
        user.save()
    except Exception as e:
        return ToJsonData().paramserr('添加失败')
    user.groups.set(groups)
    return redirect(reverse('cms:staff'))

def del_staff(request,user_id):
    if request.method == 'DELETE':
        user = MyUser.objects.filter(pk=user_id).first()
        user.is_staff = False
        user.save()
        return ToJsonData().ok()