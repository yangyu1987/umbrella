import requests
from scrapy.selector import Selector
import re

def name_start_urls():
    r = requests.get('http://www.resgain.net/xmdq.html')
    res = Selector(text=r.text)
    urls = res.xpath('//div[@class="col-xs-12"]/a/@href').extract()
    start = []
    for url in urls:
        url = 'http:'+url
        start.append(url)
    return start

def name_start():
    r = requests.get('http://www.resgain.net/xmdq.html')
    res = Selector(text=r.text)
    urls = res.xpath('//div[@class="col-xs-12"]/a/@href').extract()
    names = []
    for url in urls:
        name = re.search('//(.*?).resgain.net/name_list.html',url).group(1)
        names.append(name)
    return names