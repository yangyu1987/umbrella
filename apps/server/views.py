from django.shortcuts import render
from rest_framework import mixins,viewsets,status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ServerSerializer
from .models import Server
from .filters import ServerFilter


class ServerPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'offset'
    max_page_size = 100
    page_query_param = 'page'


class ServerViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    pagination_class = ServerPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ServerFilter
    # filter_backends = (DjangoFilterBackend, SearchFilter)
    # search_fields = ('name', 'owner', 'detail')
