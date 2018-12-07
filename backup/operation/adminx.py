from .models import CrawlerServer,CrawlerProject
import xadmin


class CrawlerServerAdmin(object):
    list_display = ['id','crawler','server', 'add_time']
    list_filter = ['id','crawler','server', 'add_time']


class CrawlerProjectAdmin(object):
    list_display = ['id','crawler','project', 'add_time']
    list_filter = ['id','crawler','project', 'add_time']


xadmin.site.register(CrawlerServer,CrawlerServerAdmin)
xadmin.site.register(CrawlerProject,CrawlerProjectAdmin)
