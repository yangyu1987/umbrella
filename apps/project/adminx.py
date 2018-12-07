# -*- coding: utf-8 -*-
# @Author: WildMan
# @Date: 2018/1/24
from .models import Project
import xadmin


class ProjectAdmin(object):
    list_display = ['id','name', 'add_time']
    list_filter = ['id','name', 'add_time']


xadmin.site.register(Project,ProjectAdmin)
