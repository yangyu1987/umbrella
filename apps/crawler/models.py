from django.db import models
from datetime import datetime
from project.models import Project
from server.models import Server

# from operation.models import CrawlerProject,CrawlerServer


class Crawler(models.Model):
    crawlerName = models.CharField(verbose_name='工程名（英文）', default='', max_length=100, unique=True,null=True, blank=True)
    webName = models.CharField(verbose_name='网站名',default='',max_length=100)
    description = models.CharField(verbose_name='描述',max_length=255, null=True, blank=True)
    type = models.IntegerField(verbose_name='爬虫类型',default =0,choices=((0,'定向爬虫'),(1,'漫游爬虫'),(2,'自定义爬虫')))
    egg = models.CharField(verbose_name='egg文件',max_length=255, null=True, blank=True)
    file = models.FileField(upload_to='projects/',default='', null=True, blank=True)
    conf = models.TextField(verbose_name='配置',default='', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    built_at = models.DateTimeField(default=None, blank=True, null=True)
    generated_at = models.DateTimeField(default=None, blank=True, null=True)
    server = models.ManyToManyField(Server,through='CrawlerServer')
    project = models.ManyToManyField(Project,through='CrawlerProject')


    class Meta:
        verbose_name = '爬虫'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.crawlerName)


class CrawlerServer(models.Model):
    # 多对多 服务器 爬虫表
    crawler = models.ForeignKey(Crawler,on_delete=models.CASCADE)
    server = models.ForeignKey(Server,on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = '爬虫-服务器'
        verbose_name_plural = verbose_name
        unique_together = ('crawler', 'server')

    def __str__(self):
        return str(self.server)


class CrawlerProject(models.Model):
    # 多对多 项目 爬虫表
    crawler = models.ForeignKey(Crawler,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = '爬虫-项目'
        verbose_name_plural = verbose_name
        unique_together = ('crawler', 'project')

    def __str__(self):
        return str(self.project)

