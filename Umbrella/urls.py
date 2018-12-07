"""Umbrella URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import xadmin

from django.conf.urls import url,include

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token


#viewset
from project.views import ProjectViewSet
from crawler.views import CrawlerViewSet,CrawlerServerViewSet,CrawlerProjectViewSet,ServerCpuRamViewSet
from crawler.views import CrawlerListViewSet,SpiderListViewSet,SpiderStartViewSet,JobListViewSet,JobLogViewSet
from server.views import ServerViewSet

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# 项目模块
router.register(r'project', ProjectViewSet, base_name='project')
# 爬虫模块
router.register(r'crawler', CrawlerViewSet, base_name='crawler')
# 服务器模块
router.register(r'server', ServerViewSet, base_name='server')
router.register(r'serverCpu', ServerCpuRamViewSet, base_name='serverCpu')
# 操作模块
router.register(r'action/server', CrawlerServerViewSet, base_name='actionServer')
router.register(r'action/project', CrawlerProjectViewSet, base_name='actionProject')
# 爬虫控制模块
router.register(r'api/crawlerList', CrawlerListViewSet, base_name='crawlerlist')
router.register(r'api/spiderList', SpiderListViewSet, base_name='spiderList')
router.register(r'api/spiderStart', SpiderStartViewSet, base_name='spiderStart')
router.register(r'api/jobList', JobListViewSet, base_name='jobList')
router.register(r'api/jobLog', JobLogViewSet, base_name='jobLog')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('doc/', include_docs_urls(title='保护伞')),
    # path('action/crawlerList/', CrawlerListView.as_view(), name='crawlerlist'),
    # path('action/spiderList/', SpiderListView.as_view(), name='spiderList'),
    # path('action/spiderStart/',SpiderStartView.as_view(), name='spiderStart'),
    # path('action/jobList/',JobListView.as_view(), name='JobList'),
    # path('action/jobLog/',JobLogView.as_view(), name='JobLog'),
    # 自带认证接口
    # url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^login/', obtain_jwt_token),
    url(r'^', include(router.urls)),
    # url(r'project/', Project),
]
