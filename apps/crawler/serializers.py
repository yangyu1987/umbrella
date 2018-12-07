from rest_framework import serializers
from .models import Crawler,CrawlerProject,CrawlerServer
from rest_framework.validators import UniqueTogetherValidator

from project.serializers import ProjectSerializer
from server.serializers import ServerSerializer

from server.models import Server
from utils.common import get_scrapyd,log_url

from requests.exceptions import ConnectionError
import requests

class CrawlerSerializer(serializers.ModelSerializer):
    # 格式化时间输出
    add_time = serializers.DateTimeField(format="%Y-%m-%d ", read_only=True, default='')
    built_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True, default='')
    generated_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True, default='')
    egg = serializers.CharField(read_only=True, default='')

    class Meta:
        model = Crawler
        fields = '__all__'


class CrawlerDtSerializer(serializers.ModelSerializer):
    # 格式化时间输出
    add_time = serializers.DateTimeField(format="%Y-%m-%d ", read_only=True, default='')
    built_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True, default='')
    generated_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True, default='')

    server = ServerSerializer(many=True)
    project = ProjectSerializer(many=True)

    class Meta:
        model = Crawler
        fields = '__all__'


class CrawlerServerSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True, default='')

    class Meta:
        model = CrawlerServer
        validators = [
            UniqueTogetherValidator(
                queryset=CrawlerServer.objects.all(),
                fields=('crawler', 'server'),
                message="已存在此服务和爬虫"
            )
        ]
        fields = '__all__'


class CrawlerServerDtSerializer(serializers.ModelSerializer):
    """
        服务器详情
        """
    server = ServerSerializer()

    class Meta:
        model = CrawlerServer
        fields = '__all__'


class CrawlerProjectSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True, default='')

    class Meta:
        model = CrawlerProject
        validators = [
            UniqueTogetherValidator(
                queryset=CrawlerProject.objects.all(),
                fields=('crawler', 'project'),
                message="已存在此项目和爬虫"
            )
        ]
        fields = '__all__'


class CrawlerProjectDtSerializer(serializers.ModelSerializer):
    """
        项目详情
        """
    project = ProjectSerializer()

    class Meta:
        model = CrawlerProject
        fields = '__all__'


class CrawlerListSerializer(serializers.Serializer):
    server = serializers.CharField(max_length=10, label='服务器ID',required=True,allow_blank=False,error_messages={
        "blank": "请传入服务器ID",
        "required": "请传入服务器ID",
    },write_only=True)
    data = serializers.DictField(read_only=True)

    def get_crawlers(self,server):
        client = Server.objects.get(id=server)
        scrapyd = get_scrapyd(client)
        try:
            crawlers = scrapyd.list_projects()
            crawlers = [{'crawler': crawler, 'id': index + 1} for index, crawler in enumerate(crawlers)]
            res = {
                "code": '1',
                "message": '请求成功',
                "result": crawlers
            }
            return res
        except ConnectionError:
            res = {
                "code": '0',
                "message": '服务器响应超时',
                "result": []
            }
            return res

    def validate(self, attrs):  # 全局钩子函数
        attrs["data"] = self.get_crawlers(attrs["server"])
        return attrs


class SpiderListSerializer(serializers.Serializer):
    server = serializers.CharField(max_length=10, label='服务器ID',required=True,allow_blank=False,error_messages={
        "blank": "请传入服务器ID",
        "required": "请传入服务器ID",
    },write_only=True)
    crawler = serializers.CharField(max_length=255, label='爬虫工程名', required=True, allow_blank=False, error_messages={
        "blank": "请传入爬虫工程名",
        "required": "请传入爬虫工程名",
    }, write_only=True)
    data = serializers.DictField(read_only=True)

    def get_spiders(self,server,crawler):
        client = Server.objects.get(id=server)
        scrapyd = get_scrapyd(client)
        try:
            spiders = scrapyd.list_spiders(crawler)
            spiders = [{'spider': spider, 'id': index + 1} for index, spider in enumerate(spiders)]
            res = {
                "code": '1',
                "message": '请求成功',
                "result": spiders
            }
            return res
        except ConnectionError:
            res = {
                "code": '0',
                "message": '服务器响应超时',
                "result": []
            }
            return res

    def validate(self, attrs):  # 全局钩子函数
        attrs["data"] = self.get_spiders(attrs["server"],attrs["crawler"])
        return attrs


class SpiderStartSerializer(serializers.Serializer):
    server = serializers.CharField(max_length=10, label='服务器ID',required=True,allow_blank=False,error_messages={
        "blank": "请传入服务器ID",
        "required": "请传入服务器ID",
    },write_only=True)
    crawler = serializers.CharField(max_length=255, label='爬虫工程名', required=True, allow_blank=False, error_messages={
        "blank": "请传入爬虫工程名",
        "required": "请传入爬虫工程名",
    }, write_only=True)
    spider = serializers.CharField(max_length=255, label='爬虫名', required=True, allow_blank=False, error_messages={
        "blank": "请传入爬虫名",
        "required": "请传入爬虫名",
    }, write_only=True)
    data = serializers.DictField(read_only=True)

    def spiders_start(self,server,crawler,spider):
        client = Server.objects.get(id=server)
        scrapyd = get_scrapyd(client)
        try:
            job = scrapyd.schedule(crawler, spider)
            res = {
                "code": '1',
                "message": '请求成功',
                "result": {
                    'job': job
                }
            }
            return res

        except ConnectionError:
            res = {
                "code": '0',
                "message": '服务器响应超时',
                "result": {}
            }
            return res

    def validate(self, attrs):  # 全局钩子函数
        attrs["data"] = self.spiders_start(attrs["server"],attrs["crawler"],attrs["spider"])
        return attrs


class JobListSerializer(serializers.Serializer):
    server = serializers.CharField(max_length=10, label='服务器ID',required=True,allow_blank=False,error_messages={
        "blank": "请传入服务器ID",
        "required": "请传入服务器ID",
    },write_only=True)
    crawler = serializers.CharField(max_length=255, label='爬虫工程名', required=True, allow_blank=False, error_messages={
        "blank": "请传入爬虫工程名",
        "required": "请传入爬虫工程名",
    }, write_only=True)
    data = serializers.DictField(read_only=True)

    def get_jobs(self,server,crawler):
        client = Server.objects.get(id=server)
        scrapyd = get_scrapyd(client)
        try:
            result = scrapyd.list_jobs(crawler)
            jobs = []
            statuses = ['pending', 'running', 'finished']
            for statu in statuses:
                for job in result.get(statu):
                    job['status'] = statu
                    jobs.append(job)

            res = {
                "code": '1',
                "message": '请求成功',
                "result": {
                    'jobs': jobs
                }
            }
            return res
        except ConnectionError:
            res = {
                "code": '0',
                "message": '服务器响应超时',
                "result": {}
            }
            return res

    def validate(self, attrs):  # 全局钩子函数
        attrs["data"] = self.get_jobs(attrs["server"],attrs["crawler"])
        return attrs


class JobLogSerializer(serializers.Serializer):
    server = serializers.CharField(max_length=10, label='服务器ID', required=True, allow_blank=False, error_messages={
        "blank": "请传入服务器ID",
        "required": "请传入服务器ID",
    }, write_only=True)
    crawler = serializers.CharField(max_length=255, label='爬虫工程名', required=True, allow_blank=False, error_messages={
        "blank": "请传入爬虫工程名",
        "required": "请传入爬虫工程名",
    }, write_only=True)
    spider = serializers.CharField(max_length=255, label='爬虫名', required=True, allow_blank=False, error_messages={
        "blank": "请传入爬虫名",
        "required": "请传入爬虫名",
    }, write_only=True)
    job = serializers.CharField(max_length=255, label='任务ID', required=True, allow_blank=False, error_messages={
        "blank": "请传入任务ID",
        "required": "请传入任务ID",
    }, write_only=True)
    data = serializers.DictField(read_only=True)

    def get_jobs_logs(self,server,crawler,spider,job):
        client = Server.objects.get(id=server)
        # 获取log地址
        url = log_url(client.ip, client.port, crawler, spider, job)
        try:
            # get last 1000 bytes of log
            response = requests.get(url, timeout=3)
            # Get encoding
            encoding = response.apparent_encoding
            # log not found
            if response.status_code == 404:
                res = {
                    "code": '2',
                    "message": '404未找到日志',
                    "result": {}
                }
                return res
            # bytes to string
            text = response.content.decode(encoding, errors='replace')
            res = {
                "code": '1',
                "message": '请求成功',
                "result": text
            }
            return res

        except requests.ConnectionError:
            res = {
                "code": '0',
                "message": '服务器响应超时',
                "result": {}
            }
            return res

    def validate(self, attrs):  # 全局钩子函数
        attrs["data"] = self.get_jobs_logs(attrs["server"],attrs["crawler"],attrs["spider"],attrs["job"])
        return attrs
