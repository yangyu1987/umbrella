#-*- encoding: utf-8 -*-
'''
MoJiWeather.py
Created on 2018/11/2714:09
Copyright (c) 2018/11/27
'''
import scrapy,datetime
from WeatherSpider.items import WeatherspiderItem
from config.config import province_dict
import logging
class MoJiWeatherSpider(scrapy.Spider):


    name = "MoJiWeatherSpider"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "PHPSESSID=if8uq5fdj2mhfsa1l6k5ies3e0; Hm_lvt_49e9e3e54ae5bf8f8c637e11b3994c74=1543283208; _ga=GA1.2.908258878.1543283209; _gid=GA1.2.797083112.1543283209; liveview_page_cursor=eyJtaW5JZCI6ODE2ODczOTYsIm1heElkIjo4MTczNjgyOCwibWluQ3JlYXRlVGltZSI6MTUwNjQ3MzY0MTAwMCwibWF4Q3JlYXRlVGltZSI6MTUwNzE3Mzk3NDAwMH0%3D; PHPSESSID=if8uq5fdj2mhfsa1l6k5ies3e0; moji_setting=%7B%22internal_id%22%3A34%7D; Hm_lvt_f943519a2c87edfe58584a4a20bc11bb=1543283180,1543290792; Hm_lpvt_f943519a2c87edfe58584a4a20bc11bb=1543290792; _gat=1; Hm_lpvt_49e9e3e54ae5bf8f8c637e11b3994c74=1543290868",
        "Host": "tianqi.moji.com",
        "Referer": "https://tianqi.moji.com/today/china",
        "Upgrade-Insecure-Requests": "1",
        }

    start_urls = [
        "https://tianqi.moji.com/today/china/anhui",
        "https://tianqi.moji.com/today/china/beijing",
        "https://tianqi.moji.com/today/china/chongqing",
        "https://tianqi.moji.com/today/china/fujian",
        "https://tianqi.moji.com/today/china/gansu",
        "https://tianqi.moji.com/today/china/guangdong",
        "https://tianqi.moji.com/today/china/guangxi",
        "https://tianqi.moji.com/today/china/guizhou",
        "https://tianqi.moji.com/today/china/hainan",
        "https://tianqi.moji.com/today/china/hebei",
        "https://tianqi.moji.com/today/china/henan",
        "https://tianqi.moji.com/today/china/hubei",
        "https://tianqi.moji.com/today/china/hunan",
        "https://tianqi.moji.com/today/china/heilongjiang",
        "https://tianqi.moji.com/today/china/jilin",
        "https://tianqi.moji.com/today/china/jiangsu",
        "https://tianqi.moji.com/today/china/jiangxi",
        "https://tianqi.moji.com/today/china/liaoning",
        "https://tianqi.moji.com/today/china/inner-mongolia",
        "https://tianqi.moji.com/today/china/ningxia",
        "https://tianqi.moji.com/today/china/qinghai",
        "https://tianqi.moji.com/today/china/shandong",
        "https://tianqi.moji.com/today/china/shanxi",
        "https://tianqi.moji.com/today/china/shaanxi",
        "https://tianqi.moji.com/today/china/shanghai",
        "https://tianqi.moji.com/today/china/sichuan",
        "https://tianqi.moji.com/today/china/tianjin",
        "https://tianqi.moji.com/today/china/tibet",
        "https://tianqi.moji.com/today/china/xinjiang",
        "https://tianqi.moji.com/today/china/yunnan",
        "https://tianqi.moji.com/today/china/zhejiang",
    ]


    from scrapy.settings import Settings
    settings=Settings()
    settings.set('CONCURRENT_REQUESTS',1)

    def start_requests(self):
        pages = []
        for request_url in self.start_urls:
            page = self.getRequest(request_url)
            pages.append(page)
        return pages

    def getRequest(self, url):
        page = scrapy.Request(url,callback=self.parse,headers=self.headers,dont_filter=True)
        return page

    def parse(self, response):
        item = WeatherspiderItem()

        try:
            area_lis = response.xpath('//div[@class="city_hot"]/ul/li')



            if area_lis:
                for area_li in area_lis:
                    #print(area_li)
                    area_href = area_li.xpath('./a/@href').extract_first()
                    #print(area_href)
                    area_province_pinyin = str(response.url).split('/')[-1]
                    area_province = province_dict[area_province_pinyin]
                    area_name = area_li.xpath('./a/text()').extract_first()
                    #print(area_name)

                    item['area_province'] = area_province
                    item['area_url'] = area_href.replace("'","''")
                    item['area_name'] = area_name

                    yield item
            else:
                logging.error("%s 没有数据据！" %(str(response.url).split('/')[-1]))
        except Exception as e:
            logging.error("%s 数据获取异常！异常为%s" %(str(response.url).split('/')[-1],e))







