from django.shortcuts import render
from rest_framework import mixins,viewsets,status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ServerSerializer,ServerStatusSerializer,CpuRamSerializer
from .models import Server
from .filters import ServerFilter


class ServerPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'offset'
    max_page_size = 100
    page_query_param = 'page'


class ServerViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    pagination_class = ServerPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ServerFilter
    # filter_backends = (DjangoFilterBackend, SearchFilter)
    # search_fields = ('name', 'owner', 'detail')


class ServerStatusViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
   服务器状态
   :param client_id: client id
   """
    queryset = ''
    serializer_class = ServerStatusSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class ServerCpuRamViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
   服务器CPU RAM 信息
   :param client_id: client id
   """
    queryset = ''
    serializer_class = CpuRamSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
