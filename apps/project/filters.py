import django_filters
from .models import Project


class ProjectFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    owner = django_filters.CharFilter(field_name='owner', lookup_expr='icontains')

    class meta:
        model = Project
        fields = ['name','owner']
