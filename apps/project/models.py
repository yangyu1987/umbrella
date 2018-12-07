from datetime import datetime

from django.db import models


class Project(models.Model):
    name = models.CharField(verbose_name='项目名',default='',max_length=100)
    owner = models.CharField(verbose_name='所有者', default='测试用户', max_length=100)
    detail = models.TextField(verbose_name='详细描述',default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)
