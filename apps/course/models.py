from django.db import models


from django.db import models

from utils.models import BaseModel
class Teacher(BaseModel):
    name = models.CharField(max_length=50,verbose_name='讲师姓名',error_messages={
        'required':'请填写倒是名称'
    })
    positional_title = models.CharField(max_length=150,verbose_name='职称',
                                        error_messages={
                                            'required': '请填写职称'
                                        })
    profile = models.TextField(verbose_name='讲师简介',  error_messages={
                                            'required': '请填写简介'
                                        })
    avatar_url = models.URLField(verbose_name='头像url',default='',
                                 error_messages={
                                     'required': '请填写头像链接'
                                 })

    class Meta:
        db_table = 'tb_teachers'
        verbose_name = '讲师'

    def __str__(self):
        return self.name

class CourseCategory(BaseModel):
    """
    娱乐  搞笑   学习  python c++  java
    """
    name = models.CharField(max_length=80,verbose_name='课程分类',
                            error_messages={
                                'required': '请填写分类名称'
                            })


    class Meta:
        db_table = 'tb_course_category'
        verbose_name = '课程分类'

    def __str__(self):
        return self.name


# 第三章表
class Course(BaseModel):
    title = models.CharField(max_length=80, verbose_name='课程名字',error_messages={
        'required': '请填写课程标题',
        'max_length': '标题长度不能超过80'
    })
    cover_url = models.URLField(verbose_name='课程封面url',error_messages={
        'required':'请填写封面图链接'
    })
    video_url = models.URLField(verbose_name='视频url',error_messages={
        'required':'请填写视频链接'
    })
    profile = models.TextField(null=True,blank=True, verbose_name='课程简介')
    outline = models.TextField(null=True,blank=True,verbose_name='课程大纲')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL,null=True,blank=True)
    category = models.ForeignKey(CourseCategory,on_delete=models.SET_NULL,null=
                                 True,blank=True)

    class Meta:
        db_table = 'tb_course'
        verbose_name = '课程详情'

