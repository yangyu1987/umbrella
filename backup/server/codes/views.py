# -*- utf-8 -*-
from __future__ import print_function
import json, os, requests, time, pytz, pymongo, string
from os.path import join, exists
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.utils import timezone
from .models import Client, Project, Deploy, Monitor
from .response import JsonResponse
from .build import build_project, find_egg
from .utils import IGNORES, is_valid_name, copy_tree, TEMPLATES_DIR, TEMPLATES_TO_RENDER, render_template, \
    get_traceback, scrapyd_url, log_url, get_tree, get_scrapyd
from django.views.decorators.csrf import csrf_exempt
import paramiko
import re
import time
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
import shutil

def index(request):
    return render(request, 'index.html')


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    lookup_field = 'name'
    def get_msg(self, request, *args, **kwargs):
        generics.RetrieveUpdateDestroyAPIView.get(self, request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        generics.RetrieveUpdateDestroyAPIView.update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        generics.RetrieveUpdateDestroyAPIView.delete(self,request, *args, **kwargs)

class ProjectList(generics.ListAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    def get_msg(self, request, *args, **kwargs):
        path = os.path.abspath(join(os.getcwd(), 'projects'))
        files = os.listdir(path)
        project_list = []
        for file in files:
            print(file)
            if os.path.isdir(join(path, file)) and not file in IGNORES:
                project_list.append({'name': file})
                if not Project.objects.filter(name=file):
                    Project.objects.create(name=file)
        return generics.ListAPIView.get(self, request, *args, **kwargs)



class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'name'
    def get_msg(self, request, *args, **kwargs):
        path = os.path.abspath(join(os.getcwd(), 'projects'))
        project_name=self.kwargs['name']
        project_path = join(path, project_name)
        egg = find_egg(project_path)
        if egg:
            built_at = timezone.datetime.fromtimestamp(os.path.getmtime(join(project_path, egg)),
                                                       tz=pytz.timezone('PRC'))
            if not Project.objects.filter(name=project_name):
                Project(name=project_name, built_at=built_at, egg=egg).save()
                model = Project.objects.get(name=project_name)
            else:
                model = Project.objects.get(name=project_name)
                model.built_at = built_at
                model.egg = egg
                model.save()
        else:
            if not Project.objects.filter(name=project_name):
                Project(name=project_name).save()
            model = Project.objects.get(name=project_name)
        data = model_to_dict(model)
        Response(data)


    def update(self, request, *args, **kwargs):
        project_name=self.kwargs['name']
        path = os.path.abspath(join(os.getcwd(), 'projects'))
        project_path = join(path, project_name)
        description =request.POST.get('description')
        build_project(project_name)
        egg = find_egg(project_path)
        if not egg:
            return JsonResponse({'message': 'egg not found'})
        built_at = timezone.now()
        if not Project.objects.filter(name=project_name):
            Project(name=project_name, description=description, built_at=built_at, egg=egg).save()
            model = Project.objects.get(name=project_name)
        else:
            model = Project.objects.get(name=project_name)
            model.built_at = built_at
            model.egg = egg
            model.description = description
            model.save()
        data = model_to_dict(model)
        return Response(data)

    def delete(self, request, *args, **kwargs):
        pname=self.kwargs['name']
        project=Project.objects.get(name=pname)
        Deploy.objects.filter(project=project).delete()
        Project.objects.filter(name=pname).delete()
        path=os.path.abspath(join(os.getcwd(), 'projects',pname))
        shutil.rmtree(path)


class Client_status(generics.ListAPIView):
    queryset= ''

    def get(self, request, *args, **kwargs):
        cname= self.kwargs['name']
        client = Client.objects.get(name=cname)
        try:
            r=requests.get(scrapyd_url(client.ip, client.port), timeout=3)
            return  Response({'client':cname,'status': r.status_code,'port':'22'})

        except:
            return  Response({'client':cname,'status': r.status_code,'port':'22'})


def cpu(ip, username, password):
    host_list = ({'ip': ip, 'port': 22, 'username': username, 'password': password},)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for host in host_list:
        ssh.connect(hostname=host['ip'], port=host['port'], username=host['username'], password=host['password'])
        stdin, stdout, stderr = ssh.exec_command('cat /proc/stat | grep "cpu "')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        if str_err != "":
            print(str_err)
            continue
        else:
            cpu_time_list = re.findall('\d+', str_out)
            cpu_idle1 = cpu_time_list[3]
            total_cpu_time1 = 0
            for t in cpu_time_list:
                total_cpu_time1 = total_cpu_time1 + int(t)
        time.sleep(2)
        stdin, stdout, stderr = ssh.exec_command('cat /proc/stat | grep "cpu "')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        if str_err != "":
            print(str_err)
            continue
        else:
            cpu_time_list = re.findall('\d+', str_out)
            cpu_idle2 = cpu_time_list[3]
            total_cpu_time2 = 0
            for t in cpu_time_list:
                total_cpu_time2 = total_cpu_time2 + int(t)

        cpu_usage = round(1 - (float(cpu_idle2) - float(cpu_idle1)) / (total_cpu_time2 - total_cpu_time1), 2)
        r_msg = {'cpu': str(cpu_usage)}

        stdin, stdout, stderr = ssh.exec_command('cat /proc/meminfo')
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        if str_err != "":
            print(str_err)
            continue
        str_total = re.search('MemTotal:.*?\n', str_out).group()
        totalmem = re.search('\d+', str_total).group()
        str_free = re.search('MemFree:.*?\n', str_out).group()
        freemem = re.search('\d+', str_free).group()
        use = round(float(freemem) / float(totalmem), 2)
        r_msg['ram'] = str(use)
        ssh.close()

        return r_msg

class Client_cpus(generics. ListAPIView):

    queryset =''
    def get(self, request, *args, **kwargs):
        cname= self.kwargs['name']
        client = Client.objects.get(name=cname)
        try:
            cpu_msg = cpu(client.ip, client.username, client.password)
            return Response(cpu_msg)

        except:
            return generics.ListAPIView.get(self, request, *args, **kwargs)


class Deploys(generics.UpdateAPIView):
    serializer_class = DeploySerializer
    queryset =''
    def put(self, request, *args, **kwargs):
        path = os.path.abspath(join(os.getcwd(), 'projects'))
        pname=self.kwargs['name']
        cname=Client.objects.filter(id=request.POST.get('client')).values_list('name')[0][0]
        project_path = join(path, pname)
        description =request.POST.get('description')

        egg = find_egg(project_path)
        if not egg:
            return Response({'msg': 'egg not found'})
        egg_file = open(join(project_path, egg), 'rb')
        client = Client.objects.get(name=cname)
        project = Project.objects.get(name=pname)
        scrapyd = get_scrapyd(client)
        try:
            scrapyd.add_version(pname, int(time.time()), egg_file.read())
            deployed_at = timezone.now()
            Deploy.objects.filter(client=client, project=project).delete()
            deploy, result = Deploy.objects.update_or_create(client=client, project=project, deployed_at=deployed_at,
                                                             description=description)
            return Response(model_to_dict(deploy))
        except:
            return Response({'msg': get_traceback()})


