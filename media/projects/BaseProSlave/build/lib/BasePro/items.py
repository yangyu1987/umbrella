# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AtbItem(scrapy.Item):
    # 公司详情
    companyName = scrapy.Field() # 公司名称
    companyStatus = scrapy.Field() # 登记状态
    legalPerson = scrapy.Field() # 法人代表
    registerNum = scrapy.Field() # 注册号
    registeredCapital = scrapy.Field() # 注册地址
    companyType = scrapy.Field() # 企业类型
    registrationAuthority = scrapy.Field()# 登记机关
    establishment = scrapy.Field() # 成立日期
    operationPeriod = scrapy.Field() # 营业期限
    operationScope = scrapy.Field() # 经营范围
    registeredAddress = scrapy.Field() #注册地址
    executives = scrapy.Field() # 高管
    shareholder = scrapy.Field() # 股东
    mongo_collection = scrapy.Field() # mongo表
    crawl_time = scrapy.Field()
    crawl_time_y = scrapy.Field()
    crawl_time_m = scrapy.Field()
    crawl_time_d = scrapy.Field()
    # outboundInvestment = scrapy.Field()

    def mongo_insert(self):
        data = {
            'companyName': self['companyName'],
            'companyStatus': self['companyStatus'],
            'legalPerson': self['legalPerson'],
            'registerNum': self['registerNum'],
            'registeredCapital': self['registeredCapital'],
            'companyType': self['companyType'],
            'registrationAuthority': self['registrationAuthority'],
            'establishment': self['establishment'],
            'operationPeriod': self['operationPeriod'],
            'operationScope': self['operationScope'],
            'registeredAddress': self['registeredAddress'],
            'executives': self['executives'],
            'shareholder': self['shareholder'],
            'crawl_time': self['crawl_time'],
            'crawl_time_y': self['crawl_time_y'],
            'crawl_time_m': self['crawl_time_m'],
            'crawl_time_d': self['crawl_time_d']
        }
        mongo_collection = self['mongo_collection']
        return mongo_collection, data