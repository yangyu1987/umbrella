# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area_province = scrapy.Field()
    area_name = scrapy.Field()
    area_url = scrapy.Field()

    # print(temperature)
    # print(weather)
    # print(humidity)
    # print(wind_direction)
    # print(highest_temperature)
    # print(daytime_weather)
    # print(lowest_temperature)
    # print(night_weather)

    temperature = scrapy.Field()
    weather = scrapy.Field()
    humidity = scrapy.Field()
    wind_direction = scrapy.Field()
    highest_temperature = scrapy.Field()
    daytime_weather = scrapy.Field()
    lowest_temperature = scrapy.Field()
    night_weather = scrapy.Field()
    crawl_time = scrapy.Field()