from rest_framework import mixins,viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Crawler,CrawlerServer,CrawlerProject
from server.models import Server
from .serializers import CrawlerSerializer,CrawlerDtSerializer,CrawlerServerSerializer,CrawlerServerDtSerializer,CrawlerProjectSerializer,CrawlerProjectDtSerializer


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
            # file字段不为空需要
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


class CrawlerListView(APIView):
    """
    @指定服务器上的工程列表
    :param Server ID
    """

    def get(self, request, *args, **kwargs):
        query_dic = request.query_params
        serverId = query_dic.get('server')
        if serverId:
            client = Server.objects.get(id=serverId)
            scrapyd = get_scrapyd(client)
            try:
                projects = scrapyd.list_projects()
                return Response(projects,status=status.HTTP_200_OK)
            except ConnectionError:
                return Response({'message': 'Connect Error'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Params Error'},status=status.HTTP_200_OK)


class SpiderListView(APIView):
    """
    @爬虫列表
    :param Server ID
    :param Project ID
    """
    def get(self, request, *args, **kwargs):
        query_dic = request.query_params
        serverId = query_dic.get('server')
        projectName = query_dic.get('project')

        if query_dic:
            client = Server.objects.get(id=serverId)
            scrapyd = get_scrapyd(client)
            try:
                spiders = scrapyd.list_spiders(projectName)
                spiders = [{'spiderName': spider, 'id': index + 1} for index, spider in enumerate(spiders)]
                return Response(spiders, status=status.HTTP_200_OK)
            except ConnectionError:
                return Response({'message': 'Connect Error'}, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Params Error'}, status=status.HTTP_200_OK)


class SpiderStartView(APIView):
    """
    启动爬虫
    :param client_id: client id
    :param project_name: project name
    :param spider_name: spider name
    """
    def get(self, request, *args, **kwargs):
        query_dic = request.query_params
        serverId = query_dic.get('server')
        projectName = query_dic.get('project')
        spiderName = query_dic.get('spider')

        if query_dic:
            client = Server.objects.get(id=serverId)
            scrapyd = get_scrapyd(client)
            try:
                job = scrapyd.schedule(projectName, spiderName)
                return Response({'job': job}, status=status.HTTP_200_OK)

            except ConnectionError:
                return Response({'message': 'Connect Error'}, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Params Error'}, status=status.HTTP_200_OK)


class JobListView(APIView):
    """
    任务列表
    :param client_id: client id
    :param project_name: project name
    """
    def get(self, request, *args, **kwargs):
        query_dic = request.query_params
        serverId = query_dic.get('server')
        projectName = query_dic.get('project')

        if query_dic:
            client = Server.objects.get(id=serverId)
            scrapyd = get_scrapyd(client)
            try:
                result = scrapyd.list_jobs(projectName)
                jobs = []
                statuses = ['pending', 'running', 'finished']
                for statu in statuses:
                    for job in result.get(statu):
                        job['status'] = statu
                        jobs.append(job)
                return Response(jobs)
            except ConnectionError:
                return Response({'message': 'Connect Error'},status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Params Error'},status=status.HTTP_200_OK)


class JobLogView(APIView):
    """
    任务日志
    :param client: client id
    :param project: project name
    :param spider: spider name
    :param job_name: job id
    """
    def get(self, request, *args, **kwargs):
        query_dic = request.query_params
        serverId = query_dic.get('server')
        projectName = query_dic.get('project')
        spiderName = query_dic.get('spider')
        jobId = query_dic.get('job')
        if query_dic:
            client = Server.objects.get(id=serverId)
            # 获取log地址
            url = log_url(client.ip, client.port, projectName, spiderName, jobId)
            try:
                # get last 1000 bytes of log
                response = requests.get(url, timeout=5)
                # Get encoding
                encoding = response.apparent_encoding
                # log not found
                if response.status_code == 404:
                    return Response({'message': 'Log Not Found'}, status=status.HTTP_200_OK)
                # bytes to string
                text = response.content.decode(encoding, errors='replace')
                return Response(text)
            except requests.ConnectionError:
                return Response({'message': 'Load Log Error'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Params Error'},status=status.HTTP_200_OK)
