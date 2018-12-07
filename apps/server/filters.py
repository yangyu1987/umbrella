import django_filters
from .models import Server


class ServerFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    ip = django_filters.CharFilter(field_name='ip', lookup_expr='icontains')
    port = django_filters.CharFilter(field_name='port', lookup_expr='icontains')

    class meta:
        model = Server
        fields = ['ip','port','name']
