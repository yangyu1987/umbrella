# -*- coding:utf-8 -*-
# @Author : oldman
# @License : (C) Copyright 2015-2017, minivision

import requests
import random

def get_ip():
    ips = requests.get('http://tvp.daxiangdaili.com/ip/?tid=556633658159507&num=10&delay=1&category=2&protocol=https')
    ip = 'http://'+random.choice(ips.text.split())
    return ip
# http://tvp.daxiangdaili.com/ip/?tid=556633658159507&num=10&delay=1&category=2&protocol=https
#
# def get_ip1():
#     pass
#
# print(get_ip())
