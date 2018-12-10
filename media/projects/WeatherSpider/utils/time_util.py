#-*- encoding: utf-8 -*-
'''
time_util.py
Created on 2018/8/309:58
Copyright (c) wangjie
'''
import time

# 输入毫秒级的时间，转出正常格式的时间


def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def timeStampYear(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    YearTime = time.strftime("%Y", timeArray)
    return YearTime

def timeStampMonth(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    MonthTime = time.strftime("%m", timeArray)
    return MonthTime

def timeStampDay(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    DayTime = time.strftime("%d", timeArray)
    return DayTime

if __name__ == '__main__':
    aa = timeStampYear(1533201900000)
    print(aa)