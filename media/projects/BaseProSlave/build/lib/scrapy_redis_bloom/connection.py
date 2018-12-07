import redis, six
from scrapy.utils.misc import load_object

from . import defaults
# Default values.

SETTINGS_PARAMS_MAP = {
    'REDIS_URL': 'url',
    'REDIS_HOST': 'host',
    'REDIS_PORT': 'port',
    'REDIS_ENCODING': 'encoding',
}


def get_redis_from_settings(settings):


    params = defaults.REDIS_PARAMS.copy()
    params.update(settings.getdict('REDIS_PARAMS'))
    # XXX: Deprecate REDIS_* settings.
    for source, dest in SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val

    # Allow ``redis_cls`` to be a path to a class.
    if isinstance(params.get('redis_cls'), six.string_types):
        params['redis_cls'] = load_object(params['redis_cls'])

    return get_redis(**params)


# Backwards compatible alias.
# 调度队列的连接
reuqest_from_settings = get_redis_from_settings



DUPEFILTER_SETTINGS_PARAMS_MAP = {
    'DUPEFILTER_REDIS_URL': 'url',
    'DUPEFILTER_REDIS_HOST': 'host',
    'DUPEFILTER_REDIS_PORT': 'port',
    'DUPEFILTER_REDIS_ENCODING': 'encoding',
}


def dupefilter_get_redis_from_settings(settings):


    params = defaults.REDIS_PARAMS.copy()
    params.update(settings.getdict('DUPEFILTER_REDIS_PARAMS'))
    # XXX: Deprecate REDIS_* settings.
    for source, dest in DUPEFILTER_SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val

    # Allow ``redis_cls`` to be a path to a class.
    if isinstance(params.get('dupefilter_redis_cls'), six.string_types):
        params['dupefilter_redis_cls'] = load_object(params['dupefilter_redis_cls'])

    return get_redis(**params)

# 去重队列的配置连接
dupefilter_from_settings = dupefilter_get_redis_from_settings

# Backwards compatible alias.
from_settings = get_redis_from_settings

def get_redis(**kwargs):

    redis_cls = kwargs.pop('redis_cls', defaults.REDIS_CLS)
    url = kwargs.pop('url', None)
    if url:
        return redis_cls.from_url(url, **kwargs)
    else:
        return redis_cls(**kwargs)

