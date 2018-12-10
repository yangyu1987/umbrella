#-*- encoding: utf-8 -*-
'''
log_util.py
Created on 2018/8/210:18
Copyright (c) wangjie
'''
import configparser

from logging.handlers import TimedRotatingFileHandler

import logging
import WeatherSpider.config.config as config
import WeatherSpider.config.content as content
import time

class LogUtil:
    base_logger = content.NULL_STR

    log_dict = {}

    def get_base_logger(self,file_name):
        if LogUtil.base_logger == content.NULL_STR:
            LogUtil.base_logger = self.__get_logger(log_name='info',file_name=file_name)
        return LogUtil.base_logger

    def get_logger(self,log_name,file_name):
        '''
        实现分任务分天打印日志
        :param log_name:
        :param file_name:
        :return:
        '''
        key = log_name + file_name
        if not key in LogUtil.log_dict:
            LogUtil.log_dict[key] = self.__get_logger(log_name,file_name)
        return LogUtil.log_dict[key]


    #获取新的logger，
    def __get_new_logger(self,log_name,file_name):
        l = LogUtil()
        l.__get_logger(log_name,file_name)
        return l


    def __get_logger(self,log_name,file_name):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)

        fh = TimedRotatingFileHandler(config._LOG_DIR % (file_name),'D')
        fh.suffix = "%Y%m%d.log"
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)


        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        return self

    def info(self,msg):
        self.logger.info(msg)
        self.logger.handlers[0].flush()

    def error(self,msg):
        self.logger.error(msg)
        self.logger.handlers[0].flush()

    def exception(self,msg='Exception Logged'):
        self.logger.exception(msg)
        self.logger.handlers[0].flush()


if __name__ == '__main__':
    b = LogUtil().get_base_logger(file_name="aatest")
    print(type(b))
    b.info("111111")
    b.error("22222")
    curTime = time.strftime("%Y%m%d", time.localtime())

    c = LogUtil().get_logger('aa','bb' + curTime + '.log' )
    c.info("kkkdkkk")
