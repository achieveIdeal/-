from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
        path('detail/',views.news,name='detail'),
        path('search/',views.Search(),name='search'),
        path('newstag/',views.news,name='news'),
        path('news_detail/',views.news_detail,name='news_detail'),
        path('comment/',views.comment,name='comment'),
        path('parent_comment/',views.parentComment,name='parent_comment'),
    ]