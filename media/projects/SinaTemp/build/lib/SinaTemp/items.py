# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import pymongo


class BasetempItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #抓取时间
    crawl_time = scrapy.Field()
    # 电影标题
    title = scrapy.Field()
    # 上演时间
    time = scrapy.Field()
    # 出品地区
    area = scrapy.Field()

    mongo_collection = scrapy.Field()

    def mongo_insert(self):

        data = {
            'crawl_time':self['crawl_time'],
            'title': self['title'],
            'time': self['time'],
            'area': self['area'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection,data

class PhoneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #抓取时间
    crawl_time = scrapy.Field()
    phone_num = scrapy.Field()
    area = scrapy.Field()
    service_provider = scrapy.Field()

    mongo_collection = scrapy.Field()

    def mongo_insert(self):

        data = {
            'crawl_time':self['crawl_time'],
            'phone_num': self['phone_num'],
            'area': self['area'],
            'service_provider': self['service_provider'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection,data

class ChaohaoItem(scrapy.Item):
    # 抓取时间
    crawl_time = scrapy.Field()
    num = scrapy.Field()
    lables = scrapy.Field()

    mongo_collection = scrapy.Field()

    def mongo_insert(self):
        data = {
            'crawl_time': self['crawl_time'],
            'num': self['num'],
            'lables': self['lables'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection, data


class HcUrlItem(scrapy.Item):
    # 慧聪网企业网址
    crawl_time = scrapy.Field()
    comp_name = scrapy.Field()
    comp_id = scrapy.Field()
    comp_page = scrapy.Field()

    mongo_collection = scrapy.Field()

    def mongo_insert(self):

        data = {
            'crawl_time':self['crawl_time'],
            'comp_id': self['comp_id'],
            'comp_name': self['comp_name'],
            'comp_page': self['comp_page'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection,data


class CreditmanageMongo(scrapy.Item):
    # 慧聪网企业网址
    crawl_time = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    gender = scrapy.Field()
    age = scrapy.Field()
    tel = scrapy.Field()

    mongo_collection = scrapy.Field()

    def mongo_insert(self):
        data = {
            'crawl_time':self['crawl_time'],
            'comp_id': self['comp_id'],
            'comp_name': self['comp_name'],
            'comp_page': self['comp_page'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection,data


class CreditmanageExcel(scrapy.Item):
    # 老赖名单
    crawl_time = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    gender = scrapy.Field()
    age = scrapy.Field()
    tel = scrapy.Field()

class LierItem(scrapy.Item):
    # 老赖名单
    crawl_time = scrapy.Field()
    name = scrapy.Field()
    id_card = scrapy.Field()
    gender = scrapy.Field()
    phone = scrapy.Field()
    desc = scrapy.Field()
    image_url = scrapy.Field()
    mongo_collection = scrapy.Field()

    def mongo_insert(self):
        data = {
            'crawl_time': self['crawl_time'],
            'name': self['name'],
            'id_card': self['id_card'],
            'gender': self['gender'],
            'phone': self['phone'],
            'desc': self['desc'],
            'image_url': self['image_url'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection, data

    class LierItem(scrapy.Item):
        # 老赖名单
        crawl_time = scrapy.Field()
        name = scrapy.Field()
        id_card = scrapy.Field()
        gender = scrapy.Field()
        phone = scrapy.Field()
        desc = scrapy.Field()
        image_url = scrapy.Field()
        mongo_collection = scrapy.Field()

        def mongo_insert(self):
            data = {
                'crawl_time': self['crawl_time'],
                'name': self['name'],
                'id_card': self['id_card'],
                'gender': self['gender'],
                'phone': self['phone'],
                'desc': self['desc'],
                'image_url': self['image_url'],
            }
            mongo_collection = self['mongo_collection']

            return mongo_collection, data


class LierTempItem(scrapy.Item):
    # 老赖名单
    crawl_time = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    id_card = scrapy.Field()
    age = scrapy.Field()
    gender = scrapy.Field()
    phone = scrapy.Field()
    mongo_collection = scrapy.Field()

    def mongo_insert(self):
        data = {
            'crawl_time': self['crawl_time'],
            'name': self['name'],
            'link': self['link'],
            'age': self['age'],
            'id_card': self['id_card'],
            'gender': self['gender'],
            'phone': self['phone'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection, data


class ComTel(scrapy.Item):
    # 常用企业电话
    crawl_time = scrapy.Field()
    name = scrapy.Field()
    tel = scrapy.Field()


class KuaidiTel(scrapy.Item):
    # 常用电话
    crawl_time = scrapy.Field()
    com_name = scrapy.Field()# 快递公司名称、企业名称
    is_comp = scrapy.Field()  # 1表公司，0表示个人
    tag = scrapy.Field() # 身份标签，快递，纺织企业、消费娱乐、KTV，逾期黑名单，银行等等
    name = scrapy.Field() # 联系人姓名
    tel = scrapy.Field()# 电话号
    phone = scrapy.Field()# 手机号
    area = scrapy.Field()# 地区
    desc = scrapy.Field()# 描述
    mongo_collection = scrapy.Field()

    def mongo_insert(self):
        data = {
            'crawl_time': self['crawl_time'],
            'com_name': self['com_name'],
            'is_comp': self['is_comp'],# 是否为公司
            'tag': self['tag'],# 标签
            'name': self['name'],# 联系人
            'tel': self['tel'],
            'phone': self['phone'],
            'area': self['area'],
            'desc': self['desc'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection, data



class Baixin(scrapy.Item):
    # 百姓网合租个人房
    crawl_time = scrapy.Field()
    name = scrapy.Field()
    tel = scrapy.Field()
    area = scrapy.Field()


class Meituan(scrapy.Item):
    # 美团网酒店
    crawl_time = scrapy.Field()
    name = scrapy.Field()
    tel = scrapy.Field()
    area = scrapy.Field()
    catgory = scrapy.Field()


class ZixunItem(scrapy.Item):
    # 小视资讯频道
    kw = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    news_date = scrapy.Field()
    crawl_time = scrapy.Field()
    source = scrapy.Field()
    page_cont = scrapy.Field()
    mongo_collection = scrapy.Field()

    def mongo_insert(self):
        data = {
            'kw': self['kw'],
            'title': self['title'],
            'url': self['url'],
            'news_date': self['news_date'],
            'crawl_time': self['crawl_time'],
            'source':self['source'],
            'page_cont':self['page_cont']
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection, data


class NameItem(scrapy.Item):
    # 小视资讯频道
    name = scrapy.Field()
    mongo_collection = scrapy.Field()

    def mongo_insert(self):
        data = {
            'name': self['name'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection, data

class TelTagItem(scrapy.Item):
    # 常用电话
    crawl_time = scrapy.Field()
    shop_name = scrapy.Field()#
    tag = scrapy.Field() # 身份标签，快递，纺织企业、消费娱乐、KTV，逾期黑名单，银行等等
    tel = scrapy.Field()# 电话号
    shop_lev = scrapy.Field()# 手机号
    area = scrapy.Field()# 地区
    mongo_collection = scrapy.Field()

    def mongo_insert(self):
        data = {
            'crawl_time': self['crawl_time'],
            'shop_name': self['shop_name'],
            'tag': self['tag'],# 标签
            'tel': self['tel'],
            'shop_lev': self['shop_lev'],
            'area': self['area'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection, data


class ShopListItem(scrapy.Item):
    # 常用电话
    crawl_time = scrapy.Field()
    shop_name = scrapy.Field()#
    url = scrapy.Field() #
    area = scrapy.Field()

    def mongo_insert(self):
        data = {
            'crawl_time': self['crawl_time'],
            'shop_name': self['shop_name'],
            'tag': self['tag'],# 标签
            'tel': self['tel'],
            'shop_lev': self['shop_lev'],
            'area': self['area'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection, data

class WdzjItem(scrapy.Item):
    platname = scrapy.Field()
    rate = scrapy.Field()
    level = scrapy.Field()
    score = scrapy.Field()
    xscore = scrapy.Field()
    hscore = scrapy.Field()
    claims = scrapy.Field()
    standard = scrapy.Field()
    limit = scrapy.Field()
    operation = scrapy.Field()
    regional = scrapy.Field()
    city = scrapy.Field()
    link = scrapy.Field()
    good_preview = scrapy.Field()
    yinxiang = scrapy.Field()

    success_money = scrapy.Field()
    invent_people = scrapy.Field()
    loan_people = scrapy.Field()
    manbiaosudu = scrapy.Field()
    year_lilv = scrapy.Field()
    pingjundate = scrapy.Field()
    leiji_loan_money = scrapy.Field()
    pingji = scrapy.Field()
    paiming = scrapy.Field()
    liquidity = scrapy.Field()
    borrowing = scrapy.Field()
    investment = scrapy.Field()


class TrafficBankItem(scrapy.Item):
    product = scrapy.Field()
    name = scrapy.Field()
    sale = scrapy.Field()
    risk_rank = scrapy.Field()
    yield_rate = scrapy.Field()
    exchange_hour = scrapy.Field()
    url = scrapy.Field()
    dizeng = scrapy.Field()
    start_money = scrapy.Field()
    qudao = scrapy.Field()


class Game360Item(scrapy.Item):
    # 360手机游戏市场
    crawl_time = scrapy.Field()
    game_name = scrapy.Field()
    game_comment = scrapy.Field()
    comment_type = scrapy.Field()

    mongo_collection = scrapy.Field()

    def mongo_insert(self):
        data = {
            'crawl_time':self['crawl_time'],
            'game_name': self['game_name'],
            'game_comment': self['game_comment'],
            'comment_type': self['comment_type'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection,data


class AreaItem(scrapy.Item):
    # 行政区域划分表
    areaid = scrapy.Field()
    areano = scrapy.Field()
    areacode = scrapy.Field()
    idparentarea = scrapy.Field()
    areaname = scrapy.Field()
    areatype = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    c_time = scrapy.Field()
    mongo_collection = scrapy.Field()

    def mongo_insert(self):
        data = {
            'areaid': self['areaid'],
            'areano': self['areano'],
            'areacode': self['areacode'],
            'idparentarea': self['idparentarea'],
            'areaname': self['areaname'],
            'areatype': self['areatype'],
            'longitude': self['longitude'],
            'latitude': self['latitude'],
            'c_time': self['c_time'],
        }
        mongo_collection = self['mongo_collection']

        return mongo_collection, data