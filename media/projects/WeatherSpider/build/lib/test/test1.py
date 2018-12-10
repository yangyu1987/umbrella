#-*- encoding: utf-8 -*-
'''
test1.py
Created on 2018/11/2714:54
Copyright (c) 2018/11/27
'''

import requests

response = requests.get("https://tianqi.moji.com/today/china/zhejiang")

result = response.xpath('//*[@id="city"]/div[@class="city_hot"]/ul/li').extract()

print(result)