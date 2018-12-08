from rest_framework import mixins,viewsets,status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from .models import Crawler,CrawlerServer,CrawlerProject
from server.models import Server
from .serializers import CrawlerSerializer,CrawlerDtSerializer,CrawlerServerSerializer,CrawlerServerDtSerializer,CrawlerProjectSerializer,CrawlerProjectDtSerializer
from .serializers import CrawlerListSerializer,SpiderListSerializer,SpiderStartSerializer,JobListSerializer,JobLogSerializer,CpuRamSerializer


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 获取工程总目录
        path = os.path.abspath(join(os.getcwd(), CEAWLER_PROJECTS_FOLDER))
        file = instance.file
        if file:
            # file字段不为空
            # 解压并生成egg
            file_name = str(file).split('/')[-1] # xxx.zip
            crawler_name = str(file).split('/')[-1].split('.')[0] # xxx
            crawler_zip_path = join(path, file_name) # d://ds/ds/xxx.zip
            crawler_path = join(path, crawler_name) # d://ds/ds/xxx
            un_zip(crawler_zip_path,crawler_path)
            # 生成egg文件
            build_project(crawler_name)
            egg = find_egg(crawler_path)
            if not egg:
                # 失败 回退 删除文件夹
                if os.path.isdir(crawler_path):
                    shutil.rmtree(crawler_path)
                return Response({'message': 'egg not found'}, status=status.HTTP_201_CREATED)

            # 成功，删除压缩文件 更新字段
            os.remove(crawler_zip_path)
            instance.file = None
            instance.egg = egg
            instance.crawlerName = crawler_name
            instance.built_at = datetime.now()
            instance.save()

            return Response(serializer.data,status.HTTP_200_OK)

        # 操作
        if request.data.get('action'):
            data = {
                'action': request.data
            }
            return Response(data)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        type = request.data['type']
        # 上传爬虫
        if type == '2':
            try:
                # file_name = request.data['file'].name
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            except Exception as e:
                err = {
                    'error': '没找到文件'
                }
                return Response(err, status=status.HTTP_201_CREATED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CrawlerBuildViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class CrawlerServerViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    部署服务器
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


class CrawlerProjectViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
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


class ServerCpuRamViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = ''
    serializer_class = CpuRamSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
