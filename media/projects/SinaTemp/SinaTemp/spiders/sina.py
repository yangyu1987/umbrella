# -*- coding: utf-8 -*-
import re,pickle
import scrapy
from datetime import datetime
from SinaTemp.tools import header_list


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://mil.news.sina.com.cn/roll/index.d.html?cid=57919&page=1']
    headers = header_list.get_header()

    custom_settings = {
        # do not needs login project
        'COOKIES_ENABLED': False,
        'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],
        'RETRY_TIMES': 3,
        'DOWNLOAD_DELAY': 5,
        'ITEM_PIPELINES': {
            'SinaTemp.pipelines.MongoPipeline': 300,
        },
        # do not needs login project
        'DOWNLOADER_MIDDLEWARES': {
            'SinaTemp.middlewares.UserAgentMiddleware': 200,
            # 'SinaTemp.middlewares.ProxyMiddleware': 10,
        },
        'MONGO_DB': 'areas_list_sheng_test',
        # 'JOBDIR': 'info/hc360/002',
    }

    def parse(self, response):
        url = response.url
        titleTemps = response.xpath("//ul[@class='linkNews']/li/a")
        for titleTemp in titleTemps:
            title = titleTemp.xpath('text()').extract()[0]
            print(title)

        num = int(str(response.url).split('=')[-1])+1
        nextUrl = "http://mil.news.sina.com.cn/roll/index.d.html?page={0}".format(num)

        yield scrapy.Request(url=nextUrl, callback=self.parse)
