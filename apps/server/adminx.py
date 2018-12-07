# -*- coding: utf-8 -*-
# @Author: WildMan
# @Date: 2018/1/24
from .models import Server
import xadmin


class ServerAdmin(object):
    list_display = ['id','ip', 'port']
    list_filter = ['id','ip', 'port']


xadmin.site.register(Server, ServerAdmin)
