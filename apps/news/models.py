from utils.models import BaseModel
from django.db import models



class Comment(BaseModel):
    '''新闻评论表'''
    content = models.TextField(error_messages={
        'required':'请填写评论内容'
    })
    author = models.ForeignKey('users.MyUser', on_delete=models.SET_NULL, null=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    parents =models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return "<id:%s,content:%s,author:%s,news:%s,parents:%s>"%(self.id,self.content,self.author_id,self.news_id,self.parents)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_comment'
        verbose_name = '新闻评论表'
        verbose_name_plural = verbose_name


class Tag(BaseModel):
    '''新闻类型模型'''
    name = models.CharField(unique=True,max_length=100, verbose_name='新闻类型',error_messages={
        'required':'请填写分类名称'
    })

    def __str__(self):
        return "<%s>"%self.name

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_tag'
        verbose_name = '新闻分类表'
        verbose_name_plural = verbose_name


class News(BaseModel):
    '''新闻模型'''
    title = models.CharField(max_length=200, verbose_name='标题',error_messages={
        'required':'请填写新闻标题',
        'max_length': '标题最大长度不能超过200'
    })
    digest = models.CharField(max_length=200, verbose_name='摘要',error_messages={
        'required':'请填写新闻摘要',
        'max_length': '摘要最大长度不能超过200'
    })
    content = models.TextField(verbose_name='内容',error_messages={
        'required':'请填写新闻内容',
    })
    clicks = models.IntegerField(default=0)
    image_url = models.URLField(default='', max_length=200, verbose_name='图片链接',error_messages={
        'required':'请填写封面图链接',
    })
    author = models.ForeignKey('users.MyUser', on_delete=models.SET_NULL, null=True)
    tag = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "<%s>"%self.title

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_news'
        verbose_name = '新闻表'
        verbose_name_plural = verbose_name


class HotNews(BaseModel):
    '''热门新闻表'''
    choices = [
        (1, '第一级'),
        (2, '第二级'),
        (3, '第三级'),
    ]
    news = models.OneToOneField('News', on_delete=models.CASCADE)
    priority = models.IntegerField(choices=choices,verbose_name='优先级',error_messages={
        'required':'请填写优先级',
    })

    def __str__(self):
        return "<%s>"%self.news_id

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_hotnews'
        verbose_name = '人们新闻表'
        verbose_name_plural = verbose_name


class Banner(BaseModel):
    '''轮播图表'''
    choices = [

        (1, '第一级'),
        (2, '第二级'),
        (3, '第三级'),
        (4, '第四级'),
        (5, '第五级'),
        (6, '第六级'),
    ]

    image_url = models.URLField(default='', verbose_name='图片连接',error_messages={
        'required': '请输入图片链接'
    })
    priority = models.IntegerField(choices=choices,null=True, blank=True)
    news = models.OneToOneField('News', on_delete=models.CASCADE,error_messages={
        'required':'请输入新闻地址'
    })

    class Meta:
        ordering = ['-priority','-update_time', '-id']
        db_table = 'tb_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name


class Document(BaseModel):
    '''文档模型'''

    file_url = models.URLField(error_messages={
        'required':'请填写文档路径',
    })
    title = models.CharField(max_length=200,error_messages={
        'required':'请填写文档标题',
    })
    desc = models.CharField(max_length=200,error_messages={
        'required':'请填写文档描述',
    })
    image_url = models.URLField(error_messages={
        'required':'请填写文档图片链接',
    })
    author = models.ForeignKey('users.MyUser',on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_docs'
        verbose_name = '文档'
        verbose_name_plural = verbose_name
