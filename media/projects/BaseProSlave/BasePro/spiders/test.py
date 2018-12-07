# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import Rule
from scrapy_redis_bloom.spiders import RedisCrawlSpider
from scrapy.linkextractor import LinkExtractor
from BasePro.tools import header_list
from BasePro.items import AtbItem

from datetime import datetime


class Atb1Spider(RedisCrawlSpider):
    name = 'atb1'
    allowed_domains = ['www.atobo.com.cn']
    redis_key = 'atbredis:start_urls'
    headers = header_list.get_header()

    custom_settings = {
        # do not needs login project
        'COOKIES_ENABLED': False,
        'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],
        'RETRY_TIMES': 3,
        # 'DOWNLOAD_DELAY': 0.05,
        'ITEM_PIPELINES': {
            'BasePro.pipelines.AtbMongoPipeline': 300,
        },
        # do not needs login project
        'DOWNLOADER_MIDDLEWARES': {
            'BasePro.middlewares.UserAgentMiddleware': 200,
            'BasePro.middlewares.ProxyAbMiddleware': 10,
        },
        'MONGO_DB': 'AtbCompany1',
        # 'JOBDIR': 'info/hc360/002',
    }

    linkComp = LinkExtractor(allow=(r'Companys/s-.*/'))
    linkGs = LinkExtractor(allow=(r'GongShang/.*html'))
    rules = (
        Rule(linkComp,follow=True),
        Rule(linkGs, follow=True,callback='parseAtb'),
        # Rule(LinkExtractor(), follow=True),
    )

    def parseAtb(self,response):
        item = AtbItem()
        try:
            companyName = response.xpath('//td[contains(text(),"公司名称")]/following-sibling::td/text()').extract()[0]  # 公司名称
            item['companyName'] = companyName
        except:
            item['companyName'] = ''
        try:
            companyStatus = response.xpath('//td[contains(text(),"登记状态")]/following-sibling::td/text()').extract()[0]  # 登记状态
            item['companyStatus'] = companyStatus
        except:
            item['companyStatus'] = ''
        try:
            legalPerson = response.xpath('//td[contains(text(),"法人代表")]/following-sibling::td/text()').extract()[0]  # 法人代表
            item['legalPerson'] = legalPerson
        except:
            item['legalPerson'] = ''
        try:
            registerNum = response.xpath('//td[contains(text(),"注 册 号")]/following-sibling::td/text()').extract()[0]  # 注册号
            item['registerNum'] = registerNum
        except:
            item['registerNum'] = ''
        try:
            registeredCapital = response.xpath('//td[contains(text(),"注册地址")]/following-sibling::td/text()').extract()[0]  # 注册地址
            item['registeredCapital'] = registeredCapital
        except:
            item['registeredCapital'] = ''
        try:
            companyType = response.xpath('//td[contains(text(),"企业类型")]/following-sibling::td/text()').extract()[0]  # 企业类型
            item['companyType'] = companyType
        except:
            item['companyType'] = ''
        try:
            registrationAuthority = response.xpath('//td[contains(text(),"登记机关")]/following-sibling::td/text()').extract()[0]  # 登记机关
            item['registrationAuthority'] = registrationAuthority
        except:
            item['registrationAuthority'] = ''
        try:
            establishment = response.xpath('//td[contains(text(),"成立日期")]/following-sibling::td/text()').extract()[0]  # 成立日期
            item['establishment'] = establishment
        except:
            item['establishment'] = ''
        try:
            operationPeriod = response.xpath('//td[contains(text(),"营业期限")]/following-sibling::td/text()').extract()[0]  # 营业期限
            item['operationPeriod'] = operationPeriod
        except:
            item['operationPeriod'] = ''
        try:
            operationScope = response.xpath('//td[contains(text(),"经营范围")]/following-sibling::td/text()').extract()[0]  # 经营范围
            item['operationScope'] = operationScope
        except:
            item['operationScope'] = ''
        try:
            registeredAddress = response.xpath('//td[contains(text(),"注册地址")]/following-sibling::td/text()').extract()[0]  # 注册地址
            item['registeredAddress'] = registeredAddress
        except:
            item['registeredAddress'] = ''
        try:
            gaoguan_xp_temp = response.xpath('//div[@class="manager_table"]/ul/li')
            executives = []  # 高管
            for gaoguan_xp in gaoguan_xp_temp:
                mer_job = gaoguan_xp.xpath('div/ul/li[@class="mer-job"]/text()').extract()[0]
                mer_name = gaoguan_xp.xpath('div/ul/li[@class="mer-name"]/a/text()').extract()[0]
                gaoguan_dic = {
                    '职位':mer_job,
                    '姓名':mer_name,
                }
                executives.append(gaoguan_dic)
            item['executives'] = executives
        except:
            item['executives'] = ""
        try:
            gudong_xp_temp = response.xpath('//table[@class="gudtable"]//tr[position()>1]')
            shareholder = [] # 股东
            for gudong_xp in gudong_xp_temp:
                gud_name = gudong_xp.xpath('td[@class="gud_name"]//text()').extract()[0]
                gud_renjiao = gudong_xp.xpath('td[@class="gud_renjiao"]//text()').extract()[0]
                gud_chuzhi = gudong_xp.xpath('td[@class="gud_chuzhi"]//text()').extract()[0]
                gud_cigubilv = gudong_xp.xpath('td[@class="gud_cigubilv"]//text()').extract()[0]

                gudong_dic = {
                    '股东名称': gud_name,
                    '认缴出资额': gud_renjiao,
                    '实缴出资额': gud_chuzhi,
                    '持股比例': gud_cigubilv,
                }
                shareholder.append(gudong_dic)
                item['shareholder'] = shareholder
        except:
            item['executives'] = ""

        item['mongo_collection'] = 'info'
        item['crawl_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['crawl_time_y'] = datetime.now().strftime("%Y")
        item['crawl_time_m'] = datetime.now().strftime("%m")
        item['crawl_time_d'] = datetime.now().strftime("%d")

        yield item