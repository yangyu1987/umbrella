#-*- encoding: utf-8 -*-
'''
config.py.py
Created on 2018/8/210:11
Copyright (c) wangjie
'''
#日志地址
_LOG_DIR = "D:/tmp/logs/%s"

#数据地址
_LOCAL_DATA_DIR = ""

#mysql配置
_MYSQL_CONFG = {'HOST':'localhost','USER':'root','PASSWD':'12345678','DB':'weather','CHARSET':'utf8','PORT':3306}

#MONGO配置

_MONGO_CONFG = {}

province_dict = {
    "anhui":"安徽",
    "beijing":"北京",
    "chongqing":"重庆",
    "fujian":"福建",
    "gansu":"甘肃",
    "guangdong":"广东",
    "guangxi":"广西",
    "guizhou":"贵州",
    "hainan":"海南",
    "hebei":"河北",
    "henan":"河南",
    "hubei":"湖北",
    "hunan":"湖南",
    "heilongjiang":"黑龙江",
    "jilin":"吉林",
    "jiangsu":"江苏",
    "jiangxi":"江西",
    "liaoning":"辽宁",
    "inner-mongolia":"内蒙古",
    "ningxia":"宁夏",
    "qinghai":"青海",
    "shandong":"山东",
    "shanxi":"山西",
    "shaanxi":"陕西",
    "shanghai":"上海",
    "sichuan":"四川",
    "tianjin":"天津",
    "tibet":"西藏",
    "xinjiang":"新疆",
    "yunnan":"云南",
    "zhejiang":"浙江",
    }