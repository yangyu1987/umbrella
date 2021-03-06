from datetime import datetime

from django.db import models


class Server(models.Model):
    OsType =  models.CharField(verbose_name='服务器类型', choices=((0,'linux'),(1,'windows'),(2,'mac')),default=0, max_length=100)
    name = models.CharField(verbose_name='服务器名', default='', max_length=100)
    ip = models.CharField(verbose_name='服务器IP',default='',max_length=100)
    port = models.CharField(verbose_name='服务器端口', default='6800', max_length=100)
    userName = models.CharField(verbose_name='登陆名', default='', max_length=100)
    passWord = models.CharField(verbose_name='密码', default='', max_length=100,)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    status = models.CharField(verbose_name='服务器状态',default='',max_length=100)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)
