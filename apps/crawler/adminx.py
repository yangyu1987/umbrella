# -*- coding: utf-8 -*-
# @Author: WildMan
# @Date: 2018/1/24
from .models import Crawler,CrawlerServer,CrawlerProject
import xadmin


class CrawlerAdmin(object):
    list_display = ['id','crawlerName','type', 'add_time']
    list_filter = ['id','crawlerName','type', 'add_time']


class CrawlerServerAdmin(object):
    list_display = ['id','crawler','server', 'add_time']
    list_filter = ['id','crawler','server', 'add_time']


class CrawlerProjectAdmin(object):
    list_display = ['id','crawler','project', 'add_time']
    list_filter = ['id','crawler','project', 'add_time']


xadmin.site.register(Crawler,CrawlerAdmin)
xadmin.site.register(CrawlerServer,CrawlerServerAdmin)
xadmin.site.register(CrawlerProject,CrawlerProjectAdmin)
