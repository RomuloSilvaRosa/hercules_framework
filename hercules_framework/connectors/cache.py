import _pickle as pickle
import unittest
from dataclasses import dataclass, field

import redis
from dataslots import with_slots

from hercules_framework.models.redis import Cache as CacheModel
from hercules_framework.settings import CACHE_DB, CACHE_HOST, CACHE_PORT
from hercules_framework.utils import ExpirationTime
from hercules_framework.utils.type import check_type

StdCacheConfig = CacheModel(host=CACHE_HOST, port=CACHE_PORT, db=CACHE_DB)


@with_slots
@dataclass
class Cache:
    cache_settings: CacheModel = field(default=StdCacheConfig)
    _cache: redis.Redis = field(default=None, init=False)

    def __post_init__(self):
        self._cache = redis.Redis(**self.cache_settings.to_dict())

    def get(self, key, as_dict=False):
        data = self._cache.get(key)
        if as_dict:
            return pickle.loads(data)
        return data

    def get_keys(self, start_key: str='*'):
        return self._cache.keys(start_key)

    def save(self, key, value, exp=None):
        self.save_dict_pickle(key, exp, value)

    def save_one_day(self, key, value):
        self.save_days(key, value)

    def save_days(self, key, value: dict, days: int=1):
        self.save_dict_pickle(key, days * ExpirationTime.day, value)

    def save_dict_pickle(self, key: str, exp: int, value: dict):
        check_type(dict, value=value)
        if exp:
            self._cache.setex(key, exp, pickle.dumps(value))
        else:
            self._cache.set(key, pickle.dumps(value))


class TestCache(unittest.TestCase):
    def test_(self):
        self.test_get_all_keys()

    def test_get_all_keys(self):
        cache = Cache()
        print(cache.get_keys('*'))
