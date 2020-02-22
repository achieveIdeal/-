from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('download/', views.download, name='download'),
    path('login_out/', views.login_out, name='login_out'),
    path('documents/<int:doc_id>', views.DownLoadFile.as_view(), name='DownLoadFile'),

]
