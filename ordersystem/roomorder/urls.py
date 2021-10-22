from django.urls import path
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
    # #首页
    # path('', views.home),
    # 默认展示预定信息
    path('index/', views.index),
    # #登录界面
    path('login/', views.acc_login),
    #处理预定请求
    path('book/',views.book),
    #登出
    path('logout/',views.acc_logout),
    # 注册界面
    path('reg/',views.reg),
    path('check_username_exist/',views.check_username_exist)
]
