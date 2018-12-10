from rest_framework import serializers
from .models import Server
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator
import datetime,requests
from utils.common import scrapyd_url,cpu


class ServerSerializer(serializers.ModelSerializer):

    add_time = serializers.DateTimeField(format="%Y-%m-%d",  read_only=True, default=datetime.datetime.now)
    name = serializers.CharField(label="服务器名", required=True,
                                 validators=[
                                     UniqueValidator(queryset=Server.objects.all(), message="服务器名已存在")]
                                 )

    class Meta:
        model = Server
        validators = [
            UniqueTogetherValidator(
                queryset=Server.objects.all(),
                fields=('ip', 'port'),
                message="IP和端口已存在"
            )
        ]
        fields = '__all__'


class ServerStatusSerializer(serializers.Serializer):
    server = serializers.CharField(max_length=10, label='服务器ID', required=True, allow_blank=False, error_messages={
        "blank": "请传入服务器ID",
        "required": "请传入服务器ID",
    }, write_only=True)
    data = serializers.DictField(read_only=True)

    def get_server_status(self, server):
        client = Server.objects.get(id=server)
        # 获取服务器在线状态
        try:
            r = requests.get(scrapyd_url(client.ip, client.port), timeout=1)
            res = {
                "code": '1',
                "message": '请求成功',
                "result": {
                    "serverId":server,
                    "status":'在线'
                }
            }
            return res

        except requests.ConnectionError:
            res = {
                "code": '0',
                "message": '服务器响应超时',
                "result": {
                    "serverId": server,
                    "status":'离线'
                }
            }
            return res

    def validate(self, attrs):  # 全局钩子函数
        attrs["data"] = self.get_server_status(attrs["server"])
        return attrs


class CpuRamSerializer(serializers.Serializer):
    server = serializers.CharField(max_length=10, label='服务器ID', required=True, allow_blank=False, error_messages={
        "blank": "请传入服务器ID",
        "required": "请传入服务器ID",
    }, write_only=True)
    data = serializers.DictField(read_only=True)

    def get_cpu_ram(self,server):
        client = Server.objects.get(id=server)
        userName = client.userName
        passWord = client.passWord
        ip = client.ip
        if client.OsType in ('0','2'):
            # 获取服务器CPU内存信息
            try:
                # get Cpu Ram
                cpuRam = cpu(ip, userName, passWord)
                res = {
                    "code": '1',
                    "message": '请求成功',
                    "result": cpuRam
                }
                return res

            except requests.ConnectionError:
                res = {
                    "code": '0',
                    "message": '服务器响应超时',
                    "result": {}
                }
                return res
        else:
            res = {
                "code": '2',
                "message": 'window 主机暂时不提供',
                "result": {}
            }
            return res

    def validate(self, attrs):  # 全局钩子函数
        attrs["data"] = self.get_cpu_ram(attrs["server"])
        return attrs
