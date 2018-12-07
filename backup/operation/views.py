from rest_framework import mixins,viewsets,status
from .models import CrawlerServer,CrawlerProject
from .serializers import CrawlerServerSerializer,CrawlerProjectSerializer,CrawlerProjectDtSerializer,CrawlerServerDtSerializer
from rest_framework.response import Response


from Umbrella.settings import CEAWLER_PROJECTS_FOLDER
from utils.build import build_project,find_egg
from utils.common import get_scrapyd

import os,time
from os.path import join
from datetime import datetime

from crawler.models import Crawler
from project.models import Project
from server.models import Server


class CrawlerServerViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
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
    queryset = CrawlerProject.objects.all()
    # serializer_class = CrawlerProjectSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CrawlerProjectDtSerializer
        return CrawlerProjectSerializer

