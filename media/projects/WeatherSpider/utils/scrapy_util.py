#-*- encoding: utf-8 -*-
'''
scrapy_util.py
Created on 2018/8/2815:19
Copyright (c) 2018/8/28
'''

def tx(xpath_obj):
    return ''.join(xpath_obj.extract()).strip()

def getImg(html):
    reg = r''