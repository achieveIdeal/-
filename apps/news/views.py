import datetime
import logging

from django.conf import settings
from django.views import View
from testtinymce.settings import MEDIA_URL

from . import constants
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse
from django.http import Http404, FileResponse, StreamingHttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page

from news.models import Banner, Tag, News, HotNews, Comment
from .serialize import *
from utils.resful import ToJsonData

logger = logging.getLogger('django')


# 主页127.0.0.1:8000
@cache_page(timeout=120, cache='page_cache')
def index(request):
    # 1,获取数据库里的数据
    banners = Banner.objects.select_related('news').filter(is_delete=False).only('image_url', 'news__title')
    tag = Tag.objects.filter(is_delete=False).only('id', 'name')[0:constants.BANNER_NUM]
    hotnews = HotNews.objects.filter(is_delete=False).select_related('news').only('news_id', 'news__title',
                                                                                  'news__image_url'). \
                  order_by('priority', '-news__clicks')[0:constants.HOT_NEWS_NUM]
    # 2，序列化数据
    bannerser = BannerSerialize(instance=banners, many=True)
    tagser = TagSerialize(instance=tag, many=True)
    hotser = HotNewsSerialize(instance=hotnews, many=True)
    # 3，构造context
    context = {
        'banners': bannerser.data,
        'tags': tagser.data,
        'hotnews': hotser.data
    }
    # locals()  # 获取函数体内所有变量（函数空间/域内）
    # 4,返回数据
    return render(request, 'news/index.html', context=context)


# detail/
def news(request):
    # 1,获取分类和页码,并校检

    try:
        tag_id = int(request.GET.get('tag_id', 0))
    except:
        logger.error('没有传递有效的分类id')

        tag_id = 0
    try:
        page = int(request.GET.get('page', 1))
    except:
        logger.error('没有传递有效的页码数值')
        page = 1

    # 分析前端页面需要哪些数据，针对性查找，优化sql
    newses_queryset = News.objects.filter(is_delete=False).select_related('author', 'tag'). \
        only('title', 'tag__name', 'author__username', 'create_time', 'digest', 'image_url')
    # 判断分类id是否存在，不存在则获取全部
    news = newses_queryset.filter(tag_id=tag_id) or newses_queryset.all()
    # 分页
    paginator = Paginator(news, constants.PAGE_NUM)
    # 获取当前页数
    try:
        cur_p_news = paginator.page(page)
    except EmptyPage as e:
        logger.error('页码超过最大页数')
        # 返回最后一页
        cur_p_news = paginator.page(paginator.num_pages)
    ser = NewsSerialize(instance=cur_p_news.object_list, many=ToJsonData)
    data = {
        'total_page': paginator.num_pages,
        'newses': ser.data  # 可以序列化分页结果
    }
    return ToJsonData().ok(data=data)


# news_detail/
def news_detail(request):
    '''新闻详情'''
    # 1,获取新闻id
    try:
        news_id = int(request.GET.get('news_id', 1))
    except:
        logger.error('该新闻不存在')
        raise Http404('This page not found')
    # 2,找出该新闻
    news = News.objects.filter(is_delete=False, pk=news_id). \
        only('title', 'content', 'author__username', 'tag__name', 'create_time').first()

    if not news:
        raise Http404('This page not found')
    # 3，找出该新闻额你对应的评论
    comments = Comment.objects.filter(is_delete=False, news_id=news_id).prefetch_related('news', 'author', 'parents'). \
        only('content', 'author__username', 'create_time', 'parents__author__username', 'parents__content',
             'parents_id')
    from utils.distinct import distinct_field
    try:
        commentsEnd = distinct_field(comments, 'parents_id')
    except:
        logger.error('去重失败')
        raise Http404('系统错误')
    context = {
        'news': news,  # 只有一条数据，所以要加索引
        'comments': commentsEnd,
    }
    return render(request, 'news/news_detail.html', context=context)


# comment/
@require_POST
def comment(request):
    '''评论'''
    if not request.user.is_authenticated:
        return ToJsonData().paramserr('请登录')
    try:
        content = request.POST.get('content')
        if not content:
            return ToJsonData().paramserr('请输入内容！')
        news_id = int(request.POST.get('newsId'))
    except:
        logger.error('添加评论时出现错误')
        raise Http404('系统出错！！！！')
    author = request.user

    comment = Comment.objects.create(content=content, author=author, news_id=news_id)
    comment.save()
    data = {
        'author_name': author.username,
        'create_time': comment.update_time,
        'content': content

    }
    return ToJsonData().ok(data=data)


# parent_comment/
@require_POST
def parentComment(request):
    '''添加子评论视图'''
    if not request.user.is_authenticated:
        return ToJsonData().paramserr('请登录')
    try:
        comment_id = int(request.POST.get('comment_id'))
        content = request.POST.get('content')
        if not content:
            return ToJsonData().paramserr('请输入内容')
    except:
        logger.error('获取父评论时出错')
        raise Http404('页面未找到')

    try:
        # 获取父评论
        parents = Comment.objects.get(pk=comment_id)
    except:
        logger.error('评论不存在的评论')
        return ToJsonData().paramserr('该评论不存在')
    author = request.user
    # 新增评论
    comment = Comment.objects.create(author=author, news_id=parents.news_id, content=content)
    # 添加评论的评论
    comment.parents = parents
    comment.save()
    data = {
        'content': content,
        'author': author.username,
        'create_time': comment.update_time
    }
    return ToJsonData().ok(data=data)


from haystack.views import SearchView


# search/
class Search(SearchView):
    '''新闻搜索页面'''
    template = 'news/search.html'

    def create_response(self):
        # 接收前台用户输入的查询值
        # kw='python'
        query = self.request.GET.get('q', '')
        if not query:
            show = True
            host_news = HotNews.objects.select_related('news').only('news_id', 'news__title', 'news__image_url').filter(
                is_delete=False).order_by('priority')
            paginator = Paginator(host_news, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
            try:
                page = paginator.page(int(self.request.GET.get('page', 1)))
            # 假如传的不是整数
            except PageNotAnInteger:
                # 默认返回第一页
                page = paginator.page(1)
  
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
            return render(self.request, self.template, locals())
        else:
            show = False
            return super().create_response()
