# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class BasetempPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonPipeline(object):

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        with open('hc360url.json', 'ab+') as f:
            f.write(text.encode('utf-8'))
        return item


class ImdbMongoPipeline(object):

    def __init__(self,mongo_params):
        # 初始化mongodb信息
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client[mongo_params['db']]

    def process_item(self, item, spider):
        mongo_collection, data = item.mongo_insert()
        collection = self.db[mongo_collection]
        collection.insert(data)
        return item

    @classmethod
    def from_settings(cls,settings):
        mongo_params = {
            'db':settings['MONGO_DB'],
            'collection':settings['MONGO_COLLECTION'],
        }
        return cls(mongo_params)


class MongoPipeline(object):
    # 存入mongo
    def __init__(self,mongo_params):
        # 初始化mongodb信息
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client[mongo_params['db']]

    def process_item(self, item, spider):
        mongo_collection, data = item.mongo_insert()
        collection = self.db[mongo_collection]
        collection.insert(data)
        return item

    @classmethod
    def from_settings(cls,settings):
        mongo_params = {
            'db':settings['MONGO_DB'],
            'collection':settings['MONGO_COLLECTION'],
        }
        return cls(mongo_params)


class MongoNamePipeline(object):
    # 存入mongo
    def __init__(self, mongo_params):
        # 初始化mongodb信息
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client[mongo_params['db']]

    def process_item(self, item, spider):
        mongo_collection, data = item.mongo_insert()
        collection = self.db[mongo_collection]
        if  collection.find(data).count():
            print('重复数据')
        else:
            collection.insert(data)
            print('新增数据成功')
        return item

    @classmethod
    def from_settings(cls, settings):
        mongo_params = {
            'db': settings['MONGO_DB'],
            'collection': settings['MONGO_COLLECTION'],
        }
        return cls(mongo_params)


class ExcelPipeline(object):

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        with open('hc360url.json', 'ab+') as f:
            f.write(text.encode('utf-8'))
        return item


class LierImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info): #下载图片
        try:
            for image_url in item['image_url']:
                yield scrapy.Request(image_url,meta={'item':item}) #添加meta是为了下面重命名文件名使用
        except:
            print('@@@@@====此人没有照片====@@@@@')

    def file_path(self,request,response=None,info=None):
        item=request.meta['item'] #通过上面的meta传递过来item
        filename = '{0}.jpg'.format(item['id_card'])
        return filename

