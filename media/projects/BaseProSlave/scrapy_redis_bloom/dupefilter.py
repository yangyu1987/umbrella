import time
import logging
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from .bloomfilter import BloomFilter
from . import connection
logger = logging.getLogger(__name__)


class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""

    def __init__(self, server, key, debug, bit, hash_number):
        """Initialize duplication filter

        Parameters
        ----------
        server : Redis instance
        key : str
            Where to store fingerprints
        """
        self.server = server
        self.key = key
        self.bit = bit
        self.hash_number = hash_number
        self.bf = BloomFilter(server, key, bit, hash_number)  # you can increase blockNum if your are filtering too many urls
        self.debug = debug

    @classmethod
    def from_settings(cls, settings):
        server = connection.from_settings_filter(settings)
        # create one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        key = "dupefilter:%s" % int(time.time())
        return cls(server, key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        if self.bf.exists(fp):
            logger.info(f"dupefilte: {request.url}")
            return True
        else:
            self.bf.insert(fp)
            return False
        # added = self.server.sadd(self.key, fp)
        # return not added

    def close(self, reason):
        """Delete data on close. Called by scrapy's scheduler"""
        self.clear()

    def clear(self):
        """Clears fingerprints data"""
        self.server.delete(self.key)
