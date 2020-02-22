import json
import logging
from datetime import datetime
from urllib import parse  # 处理url参数
from urllib.parse import parse_qs

import os
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
# 分页需要用到的类
from django.core.paginator import Paginator
# 转换时间类型
from django.utils.timezone import make_aware
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib import messages

from cms import constants
from djangoProjectClass import settings
from news.models import Banner
from .forms import *
from news.models import Tag, News
from utils.resful import ToJsonData
from djangoProjectClass.settings import MEDIA_ROOT, MEDIA_URL
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .serialize_ import BannaerSerial
from course.models import *
from .view_decorator import has_permission
from .verify_views import VerifyView
from fdfs_client.client import Fdfs_client

'''图片上传服务器，配置文件加载'''
FDFS_Client = Fdfs_client(settings.FDFS_CLIENT_CONF)

logger = logging.getLogger('django')


@staff_member_required(login_url='index')  # 员工限制，非员工不得进入
def index(request):
    '''后台管理主页'''
    return render(request, 'cms/index.html')


# class EditNewsView(PermissionRequiredMixin,LoginRequiredMixin,View):  #登录认证，重定向值settings中的LOGIN_URL
#     '''编辑新闻'''
#     permission_required = []
#     raise_exception = True  #抛出异常
#
#     def get_permission_required(self):
#         code = ContentType.objects.get_for_model(Tag)
#         perm = Permission.objects.filter(content_type=code).only('codename')
#         for query in perm:
#             codename = 'tag' + '.' + query.codename
#             self.permission_required.append(codename)
#
#         return self.permission_required
#
#     def get(self, request):
#         '''选择具体的某一条新闻'''
#         try:
#             news_id = int(request.GET.get('p', 1))
#             news = News.objects.get(pk=news_id)
#             if not news:
#                 categories = Tag.objects.all()
#                 context = {
#                     'categories': categories
#                 }
#                 return render(request, 'cms/writenews.html', context=context)
#
#         except:
#                 logger.error('获取新闻时发生错误')
#                 raise Http404('参数错误')
#         context = {
#             'news': news,
#             'categories': Tag.objects.all()
#         }
#         return render(request, 'cms/writenews.html', context=context)
#
#     def post(self, request):
#         '''修改新闻'''
#         forms = EditNewsForm(request.POST)
#         if forms.is_valid():
#             title = forms.cleaned_data.get('title')
#             content = forms.cleaned_data.get('content')
#             desc = forms.cleaned_data.get('desc')
#             thumbnail = forms.cleaned_data.get('thumbnail')
#
#             News.objects.update(title=title, content=content, desc=desc, thumbnail=thumbnail)
#             return ToJsonData().ok()
#         else:
#             errors = forms.get_errors()
#             return ToJsonData().paramserr(message=errors)
#
#
# def delete_news(request,news_id):
#     news = News.objects.filter(pk=news_id).first()
#     news.is_delete = True
#     news.save(update_fields=['is_delete'])
#     return ToJsonData().ok()
#
#
# @method_decorator(has_permission('cms:index', 'news.add_news'), name='dispatch')
# class WriteNewsView(View):
#     def get(self, request):
#         categories = Tag.objects.all()
#         context = {
#             'categories': categories
#         }
#         return render(request, 'cms/writenews.html', context=context)
#
#     def post(self, request):
#         forms = AddNewsForm(request.POST)
#         if forms.is_valid():
#             title = forms.cleaned_data.get('title')
#             desc = forms.cleaned_data.get('desc')
#             thumbnail = forms.cleaned_data.get('thumbnail')
#             content = forms.cleaned_data.get('content')
#             category_id = forms.cleaned_data.get('category')
#             category = Tag.objects.get(id=category_id)
#             author = request.user
#             News.objects.create(title=title, desc=desc, thumbnail=thumbnail,
#                                 content=content,
#                                 category=category,
#                                 author=author)
#
#             return ToJsonData().ok('添加成功')
#         else:
#             errors = forms.get_errors()
#
#             return ToJsonData().paramserr(errors)

class NewsView(VerifyView):
    '''新闻增删改查'''
    model = News  # 指定模型权限
    raise_exception = True

    def get(self, request):
        news_id = request.GET.get('news_id', None)
        tags = Tag.objects.filter(is_delete=False).only('name')
        if news_id:
            news = News.objects.filter(is_delete=False, pk=news_id).defer('update_time', 'create_time', ).first()
            if not news:
                return ToJsonData().paramserr('分类不存在')
            return render(request, 'cms/writenews.html', locals())
        else:
            return render(request, 'cms/writenews.html', locals())

    def post(self, request):
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        forms = AddNewsForm(data)
        if forms.is_valid():
            news = forms.save(commit=False)  # commit 为True直接提交保存
            news.author_id = request.user.id
            news.save()

            return ToJsonData().ok('添加成功')
        else:
            errors = forms.get_errors()

            return ToJsonData().paramserr(errors)

    def put(self, request, news_id):
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        forms = EditNewsForm(data)
        if forms.is_valid():
            title = forms.cleaned_data.get('title')
            content = forms.cleaned_data.get('content')
            digest = forms.cleaned_data.get('digest')
            image_url = forms.cleaned_data.get('image_url')
            tag = forms.cleaned_data.get('tag')

            news = News.objects.filter(is_delete=False, pk=news_id).first()
            news.title = title
            news.content = content
            news.digest = digest
            news.image_url = image_url
            news.tag = tag
            news.save(update_fields=[
                'title',
                'content',
                'digest',
                'image_url',
                'tag_id',
            ])

            return ToJsonData().ok()
        else:
            errors = forms.get_errors()

            return ToJsonData().paramserr(message=errors)

    def delete(self, request, news_id):
        news = News.objects.filter(pk=news_id).first()
        news.is_delete = True
        news.save(update_fields=['is_delete'])
        return ToJsonData().ok()


@method_decorator(csrf_exempt, name='dispatch')
class MarkDownUploadImage(View):
    def post(self, request):
        image_file = request.FILES.get('editormd-image-file')  # 记得这个不要写错啦
        if not image_file:
            logger.info('从前端获取图片失败')
            return JsonResponse({'success': 0, 'message': '从前端获取图片失败'})

        if image_file.content_type not in ('image/jpeg', 'image/png', 'image/gif'):
            return JsonResponse({'success': 0, 'message': '不能上传非图片文件'})

        try:  # jpg
            image_ext_name = image_file.name.split('.')[-1]  # 切割后返回列表取最后一个元素尾缀
        except Exception as e:
            logger.info('图片拓展名异常：{}'.format(e))
            image_ext_name = 'jpg'

        try:
            upload_res = FDFS_Client.upload_by_buffer(image_file.read(), file_ext_name=image_ext_name)
        except Exception as e:
            logger.error('图片上传出现异常：{}'.format(e))
            return JsonResponse({'success': 0, 'message': '图片上传异常'})
        else:
            if upload_res.get('Status') != 'Upload successed.':
                logger.info('图片上传到FastDFS服务器失败')
                return JsonResponse({'success': 0, 'message': '图片上传到服务器失败'})
            else:
                image_name = upload_res.get('Remote file_id')
                image_url = settings.FASTDFS_SERVER_DOMAIN + image_name
                return JsonResponse({'success': 1, 'message': '图片上传成功', 'url': image_url})


class NewListView(VerifyView):
    model = News
    def get(self, request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        # category有传递但是为空的字符串，所以再转换的时候会有问题，需要作出处理
        tag_id = int(request.GET.get('tag_id', 0) or 0)

        categories = Tag.objects.filter(is_delete=False)
        newses = News.objects.select_related('tag', 'author').filter(is_delete=False). \
            only('update_time', 'title', 'author__username', 'tag__name', 'id')
        try:
            start_date = datetime.strptime(start, '%Y/%m/%d')
        except Exception as e:
            logger.error('时间格式错误:{}'.format(e))
            start_date = datetime(year=2018, month=12, day=1)
            # 判断传递的过滤条件
        try:
            end_date = datetime.strptime(end, '%Y/%m/%d')
        except Exception as e:
            logger.error('时间格式错误:{}'.format(e))
            end_date = datetime.today()

        # # 时间格式要传
        # start_date = datetime.strptime(start, '%Y/%m/%d') if start else datetime(year=2019,month=12, day=1)
        # # 没有传开始时间就设置为最开始的时间
        # end_date = datetime.strptime(end, '%Y/%m/%d') if end else datetime.today()
        # # 没有传结束时间就设为今天
        newses = newses.filter(update_time__range=((make_aware(start_date), make_aware(end_date))),
                               is_delete=False)
        if title:
            newses = newses.filter(title__icontains=title, is_delete=False)

        # 可能会是None和0 不能进行过滤
        if tag_id != 0 and tag_id is not None:
            newses = newses.filter(tag_id=tag_id, is_delete=False)
        else:
            newses = newses.filter(is_delete=False)

        ''' 
            Paginator: 分页需要使用的类，从django.core.paginator导入
            newses： 可迭代对象，几需要展示的数据
            2： 每页展示的数据条数
        '''
        paginator = Paginator(newses, constants.PAGE_NUM)
        # 获取当前页的数据的对象，page：当前页
        try:
            page_obj = paginator.page(page)
        except Exception as e:
            logger.error('超过最大页数：{}'.format(e))
            page_obj = paginator.page(paginator.num_pages)

        context_data = self.get_data(paginator, page_obj)

        context = {
            'categories': categories,
            'newses': page_obj.object_list,  # 获取当前页的数据
            'paginator': paginator,
            'page_obj': page_obj,
            'category_id': tag_id,
            'title': title,
            'start': start,
            'end': end,
            'url_parse': parse.urlencode({  # 当点击下一页或页码是需传递url查询参数，否则会出现没有过滤后的结果
                'start': start or '',  # 使用&连接多个url参数
                'end': end or '',
                'title': title or '',
                'category': tag_id or ''
            })
        }
        context.update(context_data)
        return render(request, 'cms/news_list.html', context=context)

    def get_data(self, paginator, page_obj, page_news_count=3):
        """
　　　　　分页优化
        :param page_boj:当前页面对象
        :param paginator: Paginator 分页对象
        :param page_news_count: 左右两边显示多少页面(前端页数) “[1] [...] [5] [6] [7] [8] [9] [...] [99]”
        :return:
        """
        # 获取当前页码
        page_num = page_obj.number
        # 得到当前可以分为多少页，获取总页数
        count = paginator.num_pages
        # 判断分页是否显示 “ ... ”
        left_has_more = False
        right_has_more = True
        # 返回左右显示的页码区间 range(start,end+1)  如： 1 ... 5 6 7 8 9 ... 99
        # left_page_count
        # right_page_count

        # 如果当前页码 >= 最大页码 -1 - page_news_count，那么就不显示 ...
        if page_num >= count - page_news_count - 1:
            right_has_more = False
            right_page_count = range(page_num + 1, count + 1)
        else:
            right_page_count = range(page_num + 1, page_num + 1 + page_news_count)

        if page_num >= 2 + page_news_count:
            left_has_more = True
            left_page_count = range(page_num - page_news_count, page_num)
        else:
            left_page_count = range(1, page_num)
        return {
            # 是否显示 ...
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            # 左边应该显示的页码
            'left_page_count': left_page_count,
            # 右边应该显示的页码
            'right_page_count': right_page_count,
            'current': page_obj.number,
        }


# news_tags/
class NewsTags(VerifyView):
    '''新闻分类怎删改查'''
    model = Tag
    raise_exception = True  # 抛出异常

    def get(self, request):
        '''获取新闻分类'''
        categories = Tag.objects. \
            values('id', 'name'). \
            annotate(news_num=Count('news')). \
            filter(is_delete=False).order_by('-news_num')

        context = {
            'categories': categories
        }
        return render(request, 'cms/news_category.html', context=context)

    # news_tags/
    def post(self, request):
        '''添加新闻分类'''
        name = request.POST.get('name', None)
        if not name or not name.strip():
            return ToJsonData().paramserr('请填写内容')
        name = name.strip()
        exist = Tag.objects.filter(name=name, is_delete=False).exists()
        if exist:
            return ToJsonData().paramserr(message='该分类已存在')
        else:
            Tag.objects.create(name=name)
            return ToJsonData().ok(message='创建成功')

    # news_tags/<int:tag_id>
    def put(self, request):
        '''编辑新闻分类'''
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)

        forms = EditNewCoregoryForm(data)
        if forms.is_valid():
            pk = forms.cleaned_data.get('pk')
            name = forms.cleaned_data.get('name')
            name = name.strip()
            if not name:
                return ToJsonData().paramserr('请输入内容')
            tag = Tag.objects.filter(name=name).exists()
            if tag:
                return ToJsonData().paramserr('该分类已存在')
            try:
                # Tag.objects.filter(pk=pk).update(name=name)
                tag = Tag.objects.filter(pk=pk).first()
                tag.name = name
                tag.save(update_fields=['name'])
                return ToJsonData().ok(message='修改成功')
            except Exception as f:
                return ToJsonData().paramserr(message='分类不存在')
        else:
            errors = forms.get_errors()
            return ToJsonData().paramserr(message=errors)


# @require_GET
# def news_category(request):
#     categories = Tag.objects.all()
#     context = {
#         'categories': categories
#     }
#     return render(request, 'cms/news_category.html', context=context)


# @require_POST
# def add_news_category(request):
#     name = request.POST.get('name')
#     exist = Tag.objects.filter(name=name).exists()
#     if exist:
#         return ToJsonData().paramserr(message='该分类已存在')
#     else:
#         Tag.objects.create(name=name)
#         return ToJsonData().ok(message='创建成功')


# @require_POST
# def edit_news_category(request):
#     forms = EditNewCoregoryForm(request.POST)
#     if forms.is_valid():
#         pk = forms.cleaned_data.get('pk')
#         name = forms.cleaned_data.get('name')
#         try:
#             Tag.objects.filter(pk=pk).update(name=name)
#             return ToJsonData().ok(message='修改成功')
#         except Exception as f:
#             return ToJsonData().paramserr(message='该分类不存在')
#     else:
#         errors = forms.get_errors()
#         return ToJsonData().paramserr(message=errors)


# def del_news_category(request):
#     pk = request.GET.get('pk')
#     try:
#         Tag.objects.get(pk=pk).delete()
#         return ToJsonData().ok(message='删除成功')
#     except:
#         return ToJsonData().paramserr(message='该分类不存在')

@permission_required('news.change_news', login_url='/cms/')
@require_POST
def up_thumbnail(request):
    # 上传到本地
    # file = request.FILES.get('file')
    #
    # FDFS_client = Fdfs_client('/home/pyvip/tanzhou/utils/fastdfs/storage/client.conf')
    # Fdfs_client.append_by_buffer(file)
    # try:
    #     file_path = os.path.join(MEDIA_ROOT, file.name)
    #     with open(file_path, 'wb') as fp:
    #         for chunk in file.chunks():
    #             fp.write(chunk)
    # except AttributeError as f:
    #     pass
    # url = request.build_absolute_uri(MEDIA_URL + file.name)
    # return ToJsonData().ok(message='上传成功', data={'url': url})
    image_file = request.FILES.get('file')  # 记得这个不要写错啦
    if not image_file:
        logger.info('从前端获取图片失败')
        return JsonResponse({'code': 500, 'message': '从前端获取图片失败'})

    if image_file.content_type not in ('image/jpeg', 'image/png', 'image/gif'):
        return JsonResponse({'code': 500, 'message': '不能上传非图片文件'})

    try:  # jpg
        image_ext_name = image_file.name.split('.')[-1]  # 切割后返回列表取最后一个元素尾缀
    except Exception as e:
        logger.info('图片拓展名异常：{}'.format(e))
        image_ext_name = 'jpg'

    try:
        img = image_file.read()
        upload_res = FDFS_Client.upload_by_buffer(img, file_ext_name=image_ext_name)
    except Exception as e:
        logger.error('图片上传出现异常：{}'.format(e))
        return ToJsonData().servererr(message='上传图片异常')
    else:
        if upload_res.get('Status') != 'Upload successed.':
            logger.info('图片上传到FastDFS服务器失败')
            return ToJsonData().paramserr(message='上传图片失败')
        else:
            image_name = upload_res.get('Remote file_id')
            image_url = settings.FASTDFS_SERVER_DOMAIN + image_name
            return ToJsonData().ok(message='上传成功', data={'url': image_url})


# banner/<int:banner_id>/ #post get
# banner/ #put delete
class BannersView(VerifyView):
    '''轮播图管理'''
    model = Banner

    def get(self, request):
        return render(request, 'cms/banners.html')

    def post(self, request):
        forms = BannerForm(request.POST)
        if forms.is_valid():
            banner = forms.save(commit=False)
            banner.news = forms.cleaned_data.get('news_id')
            banner.save()
            return ToJsonData().ok(message='保存成功')
        else:
            error = forms.get_errors()
            return ToJsonData().paramserr(message=error)

    def delete(self, request, banner_id):
        banner = Banner.objects.filter(is_delete=False, pk=banner_id).first()
        banner.is_delete = True
        banner.save(update_fields=['is_delete'])
        return ToJsonData().ok('删除成功')

    def put(self, request, banner_id):
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        forms = BannerForm(data)
        if forms.is_valid():
            image_url = forms.cleaned_data.get('image_url')
            news_id = forms.cleaned_data.get('news_id')
            priority = forms.cleaned_data.get('priority')
            try:
                banner = Banner.objects.filter(is_delete=False, pk=banner_id).first()
                banner.image_url = image_url
                banner.news_id = news_id
                banner.priority = priority
                banner.save()
            except Exception as e:
                logger.error('获取轮播图失败：{}'.format(e))
            return ToJsonData().ok('修改成功', data={'priority': priority})
        else:
            error = forms.get_errors()
            return ToJsonData().paramserr(message=error)


# dbv写法
# def banners(request):
#     return render(request, 'cms/banners.html')
#
# def saveBanner(request):
#     forms = SaveBannerForm(request.POST)
#     if forms.is_valid():
#         priority = forms.cleaned_data.get('priority')
#         image_url = forms.cleaned_data.get('image_url')
#         news_id = forms.cleaned_data.get('news_id')
#
#         banner = Banner.objects.create(priority=priority, image_url=image_url, news_id=news_id)
#
#         return ToJsonData().ok(data={'banner_id': banner.pk})
#
#     else:
#         errors = forms.get_errors()
#         return ToJsonData().paramserr(message=errors)
#
# def deleteBanner(request):
#     banner_id = request.GET.get('banner_id')
#     Banner.objects.get(pk=banner_id).delete()
#     return ToJsonData().ok()
#
# def editBanner(request):
#     forms = EditBannerForm(request.POST)
#     if forms.is_valid():
#         pk = forms.cleaned_data.get('pk')
#         img_url = forms.cleaned_data.get('img_url')
#         link_to = forms.cleaned_data.get('link_to')
#         priority = forms.cleaned_data.get('priority')
#
#         Banner.objects.filter(pk=pk).update(img_url=img_url, priority=priority, link_to=link_to)
#         return ToJsonData().ok(data={
#             'priority': priority,
#         })
#     else:
#         errors = forms.get_errors()
#         return ToJsonData().paramserr(message=errors)

class CourseView(VerifyView):
    model = Course

    def get(self, request):
        course_id = request.GET.get('course_id', None)
        if not course_id:
            teachers = Teacher.objects.filter(is_delete=False).only('name')
            categories = CourseCategory.objects.filter(is_delete=False).only('name')

            return render(request, 'cms/pub_course.html',locals())
        course = Course.objects.select_related('teacher', 'category'). \
            filter(is_delete=False).only('teacher__name', 'category__name', 'title',
                                         'cover_url', 'video_url',
                                         'profile', 'outline').first()
        teachers = Teacher.objects.filter(is_delete=False).only('name')
        categories = CourseCategory.objects.filter(is_delete=False).only('name')
        return render(request, 'cms/pub_course.html', locals())

    def post(self, request):
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        forms = CourseForm(data)
        if forms.is_valid():
            forms.save()
            return ToJsonData().ok('保存成功')
        else:
            error = forms.get_errors()
            return ToJsonData().paramserr(error)

    def delete(self, request, course_id):
        course = Course.objects.filter(is_delete=False, pk=course_id).first()
        if course_id:
            course.is_delete = True
            course.save(update_fields=['is_delete'])
            return ToJsonData().ok('删除成功')
        else:
            return ToJsonData().paramserr('课程不存在')

    def put(self, request, course_id):
        course = Course.objects.filter(is_delete=False, pk=course_id)
        if course:
            json_data = request.body.decode('utf-8')
            data = json.loads(json_data)
            forms = CourseForm(data)
            if forms.is_valid():
                course.update(**forms.cleaned_data)
                return ToJsonData().ok('修改成功')
            else:
                error = forms.get_errors()
                return ToJsonData().paramserr(error)

        else:
            return ToJsonData().paramserr('课程不存在')


def banner_list(request):
    bannerList = Banner.objects.filter(is_delete=False).only('image_url', 'priority', 'news_id')
    banners = BannaerSerial(instance=bannerList, many=True)
    banner = banners.data
    return ToJsonData().ok(data=banner)


# def pub_course(request):
#     if request.method == 'GET':
#         categories = CourseCategory.objects.all()
#         teachers = Teacher.objects.all()
#         context = {
#             'categories': categories,
#             'teachers': teachers
#         }
#         return render(request, 'cms/pub_course.html', context=context)
#     if request.method == 'POST':
#         forms = CourseForm(request.POST)
#         if forms.is_valid():
#             title = forms.cleaned_data.get('title')
#             category_id = forms.cleaned_data.get('category')
#             teacher_id = forms.cleaned_data.get('teacher')
#             video_url = forms.cleaned_data.get('video_url')
#             cover_url = forms.cleaned_data.get('cover_url')
#             price = forms.cleaned_data.get('price')
#             duration = forms.cleaned_data.get('duration')
#             profile = forms.cleaned_data.get('profile')
#
#             try:
#                 category = CourseCategory.objects.get(pk=category_id)
#                 teacher = Teacher.objects.get(pk=teacher_id)
#
#             except:
#                 return ToJsonData().paramserr('未找到该教师或分类')
#             Course.objects.create(title=title, video_url=video_url,
#                                   cover_url=cover_url, price=price,
#                                   duration=duration, profile=profile,
#                                   teacher=teacher, category=category)
#             return ToJsonData().ok()
#         else:
#             errors = forms.get_errors()
#             return ToJsonData().paramserr(message=errors)

class CourseListView(VerifyView):
    model = Course

    def get(self, request):
        courses = Course.objects.select_related('teacher', 'category'). \
            filter(is_delete=False).only('teacher__name', 'category__name', 'title')
        return render(request, 'cms/course_list.html', locals())
