# -*- coding: utf-8 -*-

# Scrapy settings for DLQYSpider2 utils
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import time, uuid, os

BOT_NAME = ''

SPIDER_MODULES = ['.spiders', '.other_spiders']
NEWSPIDER_MODULE = '.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'DLQYSpider2 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# 下载延迟（两个url之间的延迟）
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# 是否启用cookie
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# spider中间件
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    'DLQYSpider2.middlewares.CustomDepthMiddleware': 90,
}

# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    'DLQYSpider2.middlewares.RandomUserAgent': 90,
    'DLQYSpider2.middlewares.CookieMiddleware': 543,
    # 'DLQYSpider2.middlewares.WeiXinRetryMiddleware': 630,
    'DLQYSpider2.middlewares.ProxyMiddleware': 100,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
}

SPLASH_URL = ''
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
HTTPPROXY_ENABLED = False
SPLASH_COOKIES_DEBUG = False

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# 清洗pipeline
ITEM_PIPELINES = {
    'DLQYSpider2.pipelines.NullItemFilterPipeline': 199,
    'DLQYSpider2.pipelines.CleanPipeline': 200,
    'DLQYSpider2.pipelines.AddDateFieldToHBasePipeline': 230,
    'DLQYSpider2.pipelines.RabbitMQPipeline': 235,
    'DLQYSpider2.pipelines.CounterRedisPipeline': 240
}

t_day = int(time.strftime("%Y%m%d", time.localtime()))

# 机器节点
LOG_FILE = '/var/log/spider/{0}-{1}.log'.format(t_day, uuid.uuid4())

# windows
# if not os.path.exists('log//{0}'.format(t_day)):
#     os.makedirs('log//{0}'.format(t_day))
# LOG_FILE = 'log\/{0}\/{1}.log'.format(t_day, uuid.uuid4())

LOG_LEVEL = 'INFO'
LOG_STDOUT = False
LOG_ENCODING = 'utf-8'
DOWNLOAD_TIMEOUT = 30        # 下载超时时间
# RETRY_ENABLED = True        # 是否重试
# RETRY_TIMES = 2             # 重试次数
# REDIRECT_ENABLED = True
# REDIRECT_MAX_TIMES = 5

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# -----------------------------------公共设置-------------------------------------------------
REDIS = ''
# -------------------------------------------------------------------------------------------

# --------------------下面是用于设置项目中的scrapy-redis是否将各个Spider独立去重------------------
"""
独立配置调度和去重方便后期redis出现性能不足可将种子调度队列和去重队列分散到不同的Redis实列或者集群，
避免出现redis性能瓶颈导致的爬虫效率问题
"""
# 不清空redis队列
SCHEDULER_PERSIST = True
# 使用项目中的改版redis调度队列
SCHEDULER = "DLQYSpider2.scrapy_redis.scheduler.Scheduler"
# 使用项目中的改版bloomfiler redis去重队列
DUPEFILTER_CLASS = "DLQYSpider2.scrapy_redis.dupefilter.RFPDupeFilter"
# 使用项目中改版的queue
SCHEDULER_QUEUE_CLASS = 'DLQYSpider2.scrapy_redis.queue.PriorityQueue'

# 下面是用于调度请求的配置(如有权限认证请使用URL的方式连接)
REDIS_URL = 'redis://user:@' + REDIS + ':6379?db=4'
# 下面是去重队列的配置(如有权限认证请使用URL的方式连接)
DUPEFILTER_REDIS_URL = 'redis://user:@' + REDIS + ':6379?db=3'


# 使用的哈希函数数，默认为6
BLOOMFILTER_HASH_NUMBER = 6

# Bloomfilter使用的Redis内存位，30表示2 ^ 30 = 128MB，默认为22 (1MB 可去重130W URL)
BLOOMFILTER_BIT = 22
# -------------------------------------------------------------------------------------------

# ---------------------------------其他自定义设置----------------------------------------------
# 统计item配置
COUNTER_REDIS = {
    "host": REDIS,
    "port": 6379,
    "db": 5
}

# 新浪微博的配置
SINA_WEIBO = {
    "host": REDIS,
    "port": 6379,
    "db": 6
}
REDIS_KEY = "WeiBo:weibo_id"

# Cookie池地址
GET_COOKIE_URL = "http://10.1.4.131:5000/weibo/random"
DELETE_COOKIE_URL = "http://10.1.4.131:5000/weibo/delete/{}"

# 代理配置
PROXY_SERVER = "http://http-dyn.abuyun.com:9020"
PROXY_USER = ""
PROXY_PASS = ""

# ---------------------------------chromedriver路径-------------------------------------------
WIN32_CHROME_PATH = "D:\Engineer\Anaconda3\Scripts\chromedriver.exe"
# -------------------------------------请求头-------------------------------------------------
USER_AGENTS = [
    # 添加请求头的时候注意不要添加移动端的请求头，会导致返回的内容为移动设备的
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",

    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
]
