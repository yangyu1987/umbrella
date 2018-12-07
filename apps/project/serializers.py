from rest_framework import serializers
from .models import Project
from rest_framework.validators import UniqueValidator
import datetime


class ProjectSerializer(serializers.ModelSerializer):

    add_time = serializers.DateTimeField(format="%Y-%m-%d",  read_only=True, default='')
    owner = serializers.CharField(label="创建者", help_text="创建者",  read_only=True, default='测试创建人')
    name = serializers.CharField(label="项目名", help_text="项目名", required=True,
                                 validators=[
                                     UniqueValidator(queryset=Project.objects.all(), message="用户已经存在")]
                                 )
    detail = serializers.CharField(label="项目简述", help_text="项目简述", required=False)

    # def create(self, validated_data):
    #     pass

    # def validate_name(self, name):
    #     if len(name) <1:
    #         raise serializers.ValidationError('名字过短')
    #     return name
    #
    # def validate(self, attrs):
    #     attrs['order_sn'] = generate_order_sn()
    #     del attrs['test'] # 删除在model中没有的字段
    #     return attrs

    class Meta:
        model = Project
        fields = '__all__'
