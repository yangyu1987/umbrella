# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from BasePro.tools.header_list import get_user_agent


class BaseproSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BaseproDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CookieMiddleware(object):
    # set cookie for request, most time used in the pro need login
    def process_request(self,request,spider):
        # ck = 'SINAGLOBAL=8921766109525.262.1491589733363; _s_tentry=cuiqingcai.com; Apache=7116304911733.029.1509961091600; ULV=1509961092417:19:1:1:7116304911733.029.1509961091600:1508547125886; login_sid_t=489d856c936895538d74617ada4ef0ec; cross_origin_proto=SSL; wvr=6; SCF=AsQR6i4BRxLD8_mqVTPrQ8xEH-0sid22myGpYHOykLJRbGL1Dt0ywJdDC6zvwUy1zW5h9AfPsCaJkPIIaq5B-OU.; SUHB=0OM0fxkOSDD5MV; ALF=1512740417; SUB=_2A253B3kQDeThGeNP6lcV9ijNyzuIHXVUCAdYrDV8PUJbkNBeLRnDkW09G8sf8yttzu6SU6MjFhEPgFFV1Q..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whp8H91FrFCL3XUZjgYB7Zn5JpX5oz75NHD95QfeK2fShqceK5NWs4Dqcj_i--Xi-zRiKn7i--NiK.Xi-zNi--Ri-8si-zXi--NiK.Xi-zfi--fiK.fiKnc; UOR=bbs.win10go.com,widget.weibo.com,zihaolucky.github.io'
        # ck = dict(i.strip().split('=') for i in ck.strip().split(';'))
        request.cookies = ''


class UserAgentMiddleware(object):
    # set random UserAgent for each requests
    def process_request(self,request,spider):
        user_agent = get_user_agent()
        request.headers.setdefault('User-Agent', user_agent)


class ProxyMiddleware(object):
    # set proxy for each requests

    def process_request(self,request,spider):
        # request.meta['proxy'] = 'http://39.104.50.214:8080'
        request.meta['proxy'] = 'http://183.52.12.30:808'


import base64
proxyServer = "http://http-dyn.abuyun.com:9020"
# 代理隧道验证信息
proxyUser = "H98YV6D726J78T4D"
proxyPass = "CD1DAE21CCAEE3CD"
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class ProxyAbMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth
