from django.db import models
from crawler.models import Crawler
from project.models import Project
from server.models import Server

from datetime import datetime


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
