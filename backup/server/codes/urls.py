from django.conf.urls import url
from . import views
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from django.conf.urls import url
from . import views
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from .views import *

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'client/$', ClientList.as_view()),  # 服务器端详情查询,添加
    url(r'client/(?P<name>[a-zA-Z]+)/$', ClientDetail.as_view()),  # 指定服务器端查删改（改名字和描述
    url(r'project/$', ProjectList.as_view()),  # 项目列表
    url(r'project/(?P<name>[a-zA-Z]+)/$', ProjectDetail.as_view()), # 指定项目查删改,post=>egg打包
    url(r'^client/(?P<name>[a-zA-Z]+)/status', Client_status.as_view()),  # 返回服务器状态
    url(r'^client/(?P<name>[a-zA-Z]+)/cpus', Client_cpus.as_view()),  # 返回服务器cpu等信息
    url(r'^project/(?P<name>[a-zA-Z]+)/deploy',Deploys.as_view()),  # 指定项目部署指定服务器

]



