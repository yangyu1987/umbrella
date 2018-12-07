# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class BaseproPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    # 存入mongo
    def __init__(self,mongo_params):
        # 初始化mongodb信息
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client[mongo_params['db']]

    def process_item(self, item, spider):
        mongo_collection, data = item.mongo_insert()
        collection = self.db[mongo_collection]
        if collection.find(data).count():
            print('重复数据')
        else:
            collection.insert(data)
            print('新增数据成功')
        return item

    @classmethod
    def from_settings(cls,settings):
        mongo_params = {
            'db':settings['MONGO_DB'],
            'collection':settings['MONGO_COLLECTION'],
        }
        return cls(mongo_params)


class AtbMongoPipeline(object):

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