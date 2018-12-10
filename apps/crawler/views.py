from rest_framework import mixins,viewsets,status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from .models import Crawler,CrawlerServer,CrawlerProject
from server.models import Server
from .serializers import CrawlerSerializer,CrawlerDtSerializer,CrawlerServerSerializer,CrawlerServerDtSerializer,CrawlerProjectSerializer,CrawlerProjectDtSerializer
from .serializers import CrawlerListSerializer,SpiderListSerializer,SpiderStartSerializer,JobListSerializer,JobLogSerializer,CrawlerBuildSerializer


from Umbrella.settings import CEAWLER_PROJECTS_FOLDER
from utils.common import un_zip,get_scrapyd,log_url
from utils.build import build_project,find_egg

import os,shutil,time,requests
from os.path import join
from datetime import datetime
from requests.exceptions import ConnectionError

import json


class CrawlerViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    """
    创建爬虫
    """
    queryset = Crawler.objects.all()
    # serializer_class = CrawlerSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CrawlerDtSerializer
        return CrawlerSerializer

    def create(self, request, *args, **kwargs):
        type = request.data['type']
        path = os.path.abspath(join(os.getcwd(), CEAWLER_PROJECTS_FOLDER))
        # 上传爬虫 并解压文件
        if type == '2':
            try:
                request.data['crawlerName'] = str(request.data['file'].name).split('.')[0]
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                # 建表
                self.perform_create(serializer)
                # 解压
                file_name = request.data['file'].name  # xxx.zip
                crawlerName = str(file_name).split('.')[0]  # xxx
                crawler_zip_path = join(path, file_name)  # d://ds/ds/xxx.zip
                crawler_path = join(path, crawlerName)  # d://ds/ds/xxx
                un_zip(crawler_zip_path, crawler_path)
                # 删除压缩文件
                os.remove(crawler_zip_path)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            except Exception as e:
                try:
                    # 数据库冲突
                    file_name = request.data['file'].name  # xxx.zip
                    crawler_zip_path = join(path, file_name)  # d://ds/ds/xxx.zip
                    os.remove(crawler_zip_path)
                    err = {
                        'error': '爬虫已存在'
                    }
                except Exception as e:
                    err = {
                        'error': '没找到上传文件'
                    }
                return Response(err, status=status.HTTP_201_CREATED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CrawlerBuildViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
   @打包成EGG文件
   :param crawler name
   """
    queryset = ''
    serializer_class = CrawlerBuildSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class CrawlerServerViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    @ 部署服务器
    :param crawler: client id
    :param server: server id
    """
    queryset = CrawlerServer.objects.all()
    # serializer_class = CrawlerServerSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CrawlerServerDtSerializer
        return CrawlerServerSerializer

    def create(self, request, *args, **kwargs):
        # 获取基本信息
        crawler = Crawler.objects.get(id=request.data['crawler'])
        server = Server.objects.get(id=request.data['server'])
        crawlerName = crawler.crawlerName
        # scrapyd_url = 'http://{0}:{1}'.format(server.ip,server.port)

        # 获取工程文件夹
        path = os.path.abspath(join(os.getcwd(), CEAWLER_PROJECTS_FOLDER))
        crawler_path = join(path, crawlerName)

        # 获取egg文件
        egg = find_egg(crawler_path)
        if not egg:
            return Response({'message': 'egg not found'}, status=status.HTTP_201_CREATED)
        egg_file = open(join(crawler_path, egg), 'rb')

        # 部署爬虫到主机
        scrapyd = get_scrapyd(server)
        scrapyd.add_version(crawlerName, int(time.time()), egg_file.read())

        # 更新字段
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,headers=headers)


class CrawlerProjectViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    项目归属
    """
    queryset = CrawlerProject.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CrawlerProjectDtSerializer
        return CrawlerProjectSerializer


class CrawlerListViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    @指定服务器上的工程列表
    :param Server ID
    """
    queryset = ''
    serializer_class = CrawlerListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class SpiderListViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    @爬虫列表
    :param Server ID
    :param Project ID
    """
    queryset = ''
    serializer_class = SpiderListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class SpiderStartViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    启动爬虫
    :param client_id: client id
    :param project_name: project name
    :param spider_name: spider name
    """
    queryset = ''
    serializer_class = SpiderStartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class JobListViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    任务列表
    :param client_id: client id
    :param project_name: project name
    """
    queryset = ''
    serializer_class = JobListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class JobLogViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    任务日志
    :param client: client id
    :param project: project name
    :param spider: spider name
    :param job: job id
    """
    queryset = ''
    serializer_class = JobLogSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
