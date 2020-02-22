from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.courses, name='course'),
    path('detail/<int:course_id>/', views.couresDetail, name='detail'),
]