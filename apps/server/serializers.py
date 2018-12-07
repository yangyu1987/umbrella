from rest_framework import serializers
from .models import Server
from rest_framework.validators import UniqueValidator
import datetime


class ServerSerializer(serializers.ModelSerializer):

    add_time = serializers.DateTimeField(format="%Y-%m-%d",  read_only=True, default=datetime.datetime.now)
    ip = serializers.CharField(label="服务器地址", help_text="服务器地址", default='')
    port = serializers.CharField(label="端口", help_text="端口",  default='6800')
    name = serializers.CharField(label="服务器名", help_text="服务器名", required=True,
                                 validators=[
                                     UniqueValidator(queryset=Server.objects.all(), message="服务器已存在")]
                                 )

    # def create(self, validated_data):
    #     pass

    class Meta:
        model = Server
        fields = '__all__'
