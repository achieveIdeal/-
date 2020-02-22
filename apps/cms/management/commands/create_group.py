#导入基类
from django.core.management import BaseCommand
#导入权限，分组，和权限类型模型
from django.contrib.auth.models import Permission,ContentType,Group
# 新建类，必须为Command,父目录和祖父目录必须是这样的命名
from news.models import *
from course.models import *
class Command(BaseCommand):
    '''运行manage 输入此脚本文件名称几个自动运行handle函数'''
    def handle(self, *args, **options):
        #获取编辑组的对所有编辑相关操作的content_type
        edit_content_type = [
            # 通过模型查找该模型所属的content_type
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(Tag),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher),
        ]
        #获取编辑组下的所有权限
        edit_pression = Permission.objects.filter(content_type__in=edit_content_type)
        # # 创建编辑组分组
        editgroup = Group.objects.create(name='编辑')

        #给分组添加权限
        editgroup.permissions.set(edit_pression)
        editgroup.save()
        self.stdout.write(self.style.SUCCESS('edit组创建完成'))
        # 获取财务组所有模型的content_type
        finance_content_type = [
            # '''没写，以后写'''
            # ContentType.objects.get_for_model()
        ]
        #获取相应的权限
        finance_permission = Permission.objects.filter(content_type__in=finance_content_type)
        #创建财务组分组
        financegroup = Group.objects.create(name='财务')
        #添加权限
        financegroup.permissions.set(finance_permission)
        financegroup.save()
        self.stdout.write(self.style.SUCCESS('finance组创建完成'))

        #设置管理员组
        managergroup = Group.objects.create(name='管理员')
        #将两个queryset对象合并到一起
        manager_permissions = edit_pression.union((finance_permission))
        #添加管理员权限
        managergroup.permissions.set(manager_permissions)
        managergroup.save()
        self.stdout.write(self.style.SUCCESS('manager组创建完成'))

        '''在控制台打印成功的提示文字，ERROR打印错误的提示'''
