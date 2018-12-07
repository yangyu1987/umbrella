# -*- coding:utf-8 -*-

import os
import sys

from scrapy.cmdline import execute
sys.path.append(os.path.dirname(__file__))
# execute(['scrapy','crawl','pianzi'])
# execute(['scrapy','crawl','hc360c'])
# execute(['scrapy','crawl','test'])
# execute(['scrapy','crawl','hc360'])
# execute(['scrapy','crawl','creditmanage'])
# execute("scrapy crawl creditmanage -o tel.csv -t csv".split())
# execute(['scrapy','crawl','chadianhua'])
# execute("scrapy crawl chadianhua -o com_tel.csv -t csv".split())
# execute("scrapy crawl meituan".split())
# execute("scrapy crawl zixun".split())
# execute("scrapy crawl kuaidi100".split())
# execute("scrapy crawl test".split())
# execute("scrapy crawl namestore".split())
# execute("scrapy crawl news4sk".split())
# execute("scrapy crawl dianpin".split())
# execute("scrapy crawl qq".split())
# execute("scrapy crawl wdzj".split())
# execute("scrapy crawl TrafficBank".split())

execute("scrapy crawl sina".split())
