# -*- coding:utf-8 -*-

import os
import sys

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(__file__))
# execute(['scrapy','crawl','pianzi'])
# execute(['scrapy','crawl','hc360c'])
# execute(['scrapy','crawl','test'])
# execute(['scrapy','crawl','hc360'])
# execute(['scrapy','crawl','testredis'])
execute(['scrapy','crawl','atb'])