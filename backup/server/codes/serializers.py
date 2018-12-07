from rest_framework import serializers
from .models import *
class ClientSerializer(serializers.ModelSerializer):
   class Meta:
       model =Client
       fields = '__all__'
class DeploySerializer(serializers.ModelSerializer):
   class Meta:
       model =Deploy
       fields = ('client','description')
class ProjectSerializer(serializers.ModelSerializer):
   class Meta:
       model =Project
       fields = ('name', 'description','clients','egg')





