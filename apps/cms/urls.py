from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('', views.index, name='index'),
    # 普通函数写法
    # path('category/', views.news_category, name='category'),
    # path('addcategory/', views.add_news_category, name='addcategory'),
    # path('edit_news_category/', views.edit_news_category, name='edit_news_category'),
    # path('del_news_category/', views.del_news_category, name='del_news_category'),
    # resful规范写法
    path('news_tags/', views.NewsTags.as_view(), name='news_tags'),
    path('news_tag/<int:tag_id>/', views.NewsTags.as_view(), name='del_news'),

    path('up_thumbnail/', views.up_thumbnail, name='up_thumbnail'),
    path('markdown/images/', views.MarkDownUploadImage.as_view(), name='markdown_image_upload'),

    path('banners/', views.BannersView.as_view(), name='banners'),
    path('banner/<int:banner_id>/', views.BannersView.as_view(), name='banners'),
    path('banner_list/', views.banner_list, name='banner_list'),

    # path('banners/', views.banners, name='banners'),
    # path('save_banner/', views.saveBanner, name='savebanner'),
    # path('delete_banner/', views.deleteBanner, name='delete_banner'),
    # path('edit_banner/', views.editBanner, name='eidtbanner'),

    # path('edit_news/', views.EditNewsView.as_view(), name='edit_news'),
    # path('delete_news/<int:news_id>/', views.delete_news, name='delete_news'),
    # path('writenews/', views.WriteNewsView.as_view(), name='writenews'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('new/<int:news_id>/', views.NewsView.as_view(), name='new'),
    path('news_list/', views.NewListView.as_view(), name='newslist'),

    path('courses/', views.CourseView.as_view(), name='courses'),
    path('course/<course_id>/', views.CourseView.as_view(), name='course'),
    path('course_list/', views.CourseListView.as_view(), name='course_list'),
]
from . import staff_views

# 员工管理
urlpatterns += [
    path('staff/', staff_views.staff, name='staff'),
    path('add_staff/', staff_views.AddStaff.as_view(), name='add_staff'),
    path('del_staff/<int:user_id>/', staff_views.del_staff, name='del_staff'),
]
