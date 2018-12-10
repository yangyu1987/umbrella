#-*- encoding: utf-8 -*-
'''
db_util.py
Created on 2018/8/412:33
Copyright (c) WANGJIE
'''
import config.config as config
import pymysql

class DBUtil:
    def __init__(self):
        self.db = pymysql.connect(host = config._MYSQL_CONFG['HOST'],
                                  user = config._MYSQL_CONFG['USER'],
                                  passwd = config._MYSQL_CONFG['PASSWD'],
                                  db = config._MYSQL_CONFG['DB'],
                                  port = config._MYSQL_CONFG['PORT'],
                                  charset = config._MYSQL_CONFG['CHARSET'])

    def read_one(self,sql):
        '''
        get the one return from sql executing
        :param sql:
        :return:
        '''
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def read_tuple(self,sql):
        '''
        get tuple from sql executing
        :param sql:
        :return:
        '''
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def read_dict(self,sql):
        '''
        get dict from sql executing
        :param sql:
        :return:
        '''
        self.cursor = self.db.cursor(cursor = pymysql.cursors.DictCursor)
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def executemany(self,sql,values):
        '''
        execute many and commit
        :param sql:
        :param values:
        :return:
        '''
        self.cursor = self.db.cursor()
        self.cursor.executemany(sql,values)
        self.db.commit()

    def executemany_no_commit(self,sql,values):
        '''
        execute many sqls but don't commit
        :param sql:
        :param values:
        :return:
        '''
        self.cursor = self.db.cursor()
        self.cursor.executemany(sql,values)

    def execute(self,sql):
        '''
        execute sql and commit
        :param sql:
        :return:
        '''
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)
        self.db.commit()

    def execute_no_commit(self,sql):
        '''
        execute one sql but don't commit
        :param sql:
        :return:
        '''
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)

    def commit(self):
        self.db.commit()

    def close(self):
        '''
        all for close
        :return:
        '''
        self.cursor = self.db.cursor()
        self.cursor.close()
        self.db.close()


    def rollback(self):
        '''
        rollback the connect
        :return:
        '''
        self.db.rollback()


    def rollback_close(self):
        '''
        rollback and close db connect
        :return:
        '''
        self.db.rollback()
        self.cursor = self.db.cursor()
        self.cursor.close()
        self.db.close()





if __name__ == '__main__':
    connect = DBUtil()
    area_name = connect.read_tuple('select area_url from moji_area_url where area_url is not null')
    print(list(area_name))
    # for area in area_name:
    #     print(area[0])

    # for url in url_tuple:
    #     print(str(url))
    # db1 = DBUtil()
    # at = db1.read_dict('select * from seed_url')
    # print(type(at))
    # for i in at:
    #     for j in i:
    #         print(j,'=>',i[j])
            # url_md5 => aa
            # is_run => 1
            # url_status => 1
            # fail_times => 1

    # r1 = db1.read_tuple('select url from seed_url')
    # print(r1)
    # #(('aa', 'aa', 1, 1, 1, ''),)
    # for i in r1:
    #     print(str(i))
    #
    # # db1.executemany('insert into seed_url (url,url_md5,is_run,url_status,fail_times,comment) values (%s,%s,%s,%s,%s,%s)',
    # #                 [('b','b',1,1,1,''),('c','c',1,1,1,'')])
    # import datetime
    # dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # update_sql = "update seed_url set result=0,occur_time='%s' where id='%s'"  % (dt,1)
    # DBUtil('weibo_crawl').execute(update_sql)