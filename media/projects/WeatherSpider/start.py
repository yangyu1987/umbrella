#-*- encoding: utf-8 -*-
'''
start.py
Created on 2018/11/2715:00
Copyright (c) 2018/11/27
'''

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

tmp_settings = get_project_settings()
tmp_settings['CONCURRENT_REQUESTS']= 12
process = CrawlerProcess(tmp_settings)
process.crawl("AreaWeatherSpider")
process.start()