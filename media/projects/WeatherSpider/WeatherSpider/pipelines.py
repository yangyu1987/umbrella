# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from utils.db_util import DBUtil
import logging
class WeatherspiderPipeline(object):
    def process_item(self, item, spider):
        insert = '''
        insert into moji_area_url(area_province,area_name,area_url) values ('%s','%s','%s')
        ''' %(item['area_province'],item['area_name'],item['area_url'])

        try:
            connect = DBUtil()
            connect.execute(insert)
        except Exception as e:
            logging.error(e)
            logging.error(insert)
        finally:
            connect.close()
        return item

    def getListAreaUrl(self):
        select = '''
        select area_url from moji_area_url where area_url is not null
        '''

        try:
            connect = DBUtil()
            area_tuple = connect.read_tuple(select)
            return area_tuple
        except Exception as e:
            logging.error(e)
        finally:
            connect.close()


class AreaWeatherspiderPipeline(object):
    def process_item(self, item, spider):
        insert = '''
insert into moji_area_weather (area_url,temperature,weather,humidity,wind_direction,highest_temperature,daytime_weather,lowest_temperature,night_weather,crawl_time) values
 ('%s','%s','%s','%s','%s','%s','%s','%s','%s',%s) on duplicate key update temperature=VALUES(temperature),weather=VALUES(weather),humidity=values(humidity),
 wind_direction=values(wind_direction),highest_temperature=values(highest_temperature),daytime_weather=values(daytime_weather),lowest_temperature=values(lowest_temperature),
 night_weather=values(night_weather),crawl_time=values(crawl_time)
                ''' %(item['area_url'],item['temperature'],item['weather'],item['humidity'],item['wind_direction'],
                      item['highest_temperature'],item['daytime_weather'],item['lowest_temperature'],item['night_weather'],item['crawl_time'])
        try:
            connect = DBUtil()
            connect.execute(insert)
        except Exception as e:
            logging.error(e)
            logging.error(insert)
        finally:
            connect.close()
        return item