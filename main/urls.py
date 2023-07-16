from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('course_champion/', views.course_champion, name='course_champion'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout, name='logout'),
    path('file/', views.fileInput, name='fileInput'),
    path('individual/', views.individual_tables, name='individual_tables'),
    path('download/', views.download_file, name='download_file'),
    path('password_reset/', views.password_reset, name='password_reset'),
]