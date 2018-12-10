#-*- encoding: utf-8 -*-
'''
AreaWeather.py
Created on 2018/11/2716:40
Copyright (c) 2018/11/27
'''
import scrapy,time
import logging
from WeatherSpider.items import WeatherspiderItem
from WeatherSpider.pipelines import WeatherspiderPipeline


class AreaWeatherSpider(scrapy.Spider):
    name = "AreaWeatherSpider"

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
    weather_pipeline = WeatherspiderPipeline()
    area_url_tuples = weather_pipeline.getListAreaUrl()
    start_urls = []
    for area_url_tuple in area_url_tuples:
        start_urls.append(area_url_tuple[0])

    from scrapy.settings import Settings
    settings=Settings()
    settings.set('CONCURRENT_REQUESTS',12)

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
            temperature = response.xpath('//div[@class="now"]/div[@class="info clearfix"]/em/text()').extract_first()
            weather = response.xpath('//div[@class="now"]/div[@class="info clearfix"]/b/text()').extract_first()
            humidity = response.xpath('//div[@class="now"]/div[@class="about clearfix"]/span/text()').extract_first()
            wind_direction = response.xpath('//div[@class="now"]/div[@class="about clearfix"]/em/text()').extract_first()


            highest_temperature = response.xpath('//div[@class="day"][1]/b/text()').extract_first()
            daytime_weather = response.xpath('//div[@class="day"][1]/em/text()').extract_first()
            lowest_temperature = response.xpath('//div[@class="day"][2]/b/text()').extract_first()
            night_weather = response.xpath('//div[@class="day"][2]/em/text()').extract_first()

            item["area_url"] = str(response.url).replace("'","''")
            item["temperature"] = temperature
            item["weather"] = weather
            item["humidity"] = humidity
            item["wind_direction"] = wind_direction
            item["highest_temperature"] = str(highest_temperature).replace("°","")
            item["daytime_weather"] = daytime_weather
            item["lowest_temperature"] = str(lowest_temperature).replace("°","")
            item["night_weather"] = night_weather
            item["crawl_time"] = int(time.time())
            if item["temperature"]:
                yield item
        except Exception as e:
            logging.error("%s 数据获取异常！异常为%s" %(str(response.url),e))
        # try:
        #     area_lis = response.xpath('//div[@class="now"]/div[@class="info clearfix"]/')
        #
        #
        #
        #     if area_lis:
        #         for area_li in area_lis:
        #             #print(area_li)
        #             area_href = area_li.xpath('./a/@href').extract_first()
        #             #print(area_href)
        #             area_province_pinyin = str(response.url).split('/')[-1]
        #             area_province = province_dict[area_province_pinyin]
        #             area_name = area_li.xpath('./a/text()').extract_first()
        #             #print(area_name)
        #
        #             item['area_province'] = area_province
        #             item['area_url'] = area_href.replace("'","''")
        #             item['area_name'] = area_name
        #
        #             yield item
        #     else:
        #         logging.error("%s 没有数据据！" %(str(response.url).split('/')[-1]))
        # except Exception as e:
        #     logging.error("%s 数据获取异常！异常为%s" %(str(response.url).split('/')[-1],e))
