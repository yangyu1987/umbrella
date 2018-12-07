import django_filters
from .models import Crawler


class ProjectFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class meta:
        model = Crawler
        fields = ['name']
