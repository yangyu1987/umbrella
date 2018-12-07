from rest_framework import serializers
from .models import CrawlerProject,CrawlerServer
from rest_framework.validators import UniqueTogetherValidator

from project.serializers import ProjectSerializer
from server.serializers import ServerSerializer


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
