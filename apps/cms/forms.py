from django import forms
from news.models import Banner, Tag
from utils.formserrors import FormsMixin
from news.models import News
from course.models import Course
class EditNewCoregoryForm(forms.Form,FormsMixin):
    pk = forms.IntegerField(error_messages={
        'required': '必须传入分类id'
    },required=True)
    name = forms.CharField(max_length=100,required=True)


class AddNewsForm(forms.ModelForm,FormsMixin):
    image_url = forms.URLField()
    class Meta:
        model = News
        exclude = ['author','clicks','tag'] #url先不验证
        error_messages = {
            'title': {
                'required': '请输入标题'
            },
            'desc': {
                'required': '请输入新闻详情'
            },
            'content': {
                'required': '请输入新闻内容'
            }
        }


class BannerForm(forms.ModelForm,FormsMixin):
    news_id = forms.ModelChoiceField(queryset=News.objects.only('id').filter(is_delete=False))

    class Meta:
        model = Banner
        exclude = ['update_time','create_time','news']
        error_messages = {
            'priority': {
                'required': '请输入优先级'
            },
            'link_to': {
                'required': '请输入连接跳转'
            },
            'img_url': {
                'required': '请选择图片'
            }
        }


class EditNewsForm(forms.ModelForm,FormsMixin):
    tag = forms.ModelChoiceField(queryset=Tag.objects.only('id').filter(is_delete=False) )
    image_url = forms.URLField()

    class Meta:
        model = News
        fields = ['title','digest','content']  #url还没做，先不验证
        error_messages = {
            'digest': {
                'required': '请输入新闻摘要'
            },
            'title': {
                'required': '请输入新闻标题'
            },
            'content': {
                'required': '请输入新闻内容'
            },
            'image_url': {
                'required': '请输入图片链接'
            }
        }


class CourseForm(forms.ModelForm,FormsMixin):
    teacher = forms.IntegerField()
    category = forms.IntegerField()
    class Meta:
        model = Course
        exclude = ['teacher','category','update_time']