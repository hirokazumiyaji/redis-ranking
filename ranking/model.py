# coding: utf-8

import redis


class Ranking(object):

    def __init__(self, key, user_id, client=None, **kwargs):
        self.key = key
        self.user_id = user_id
        if client:
            self.redis = client
        else:
            self.redis = redis.StrictRedis(**kwargs)

    def __get_rank(self, redis=None):
        if not redis:
            redis = self.redis
        return redis.zrevrank(self.key, self.user_id) + 1

    def __get_score(self, redis=None):
        if not redis:
            redis = self.redis
        return redis.zscore(self.key, self.user_id)

    @property
    def rank(self):
        if hasattr(self, '_rank'):
            return _rank
        self._rank = self.__get_rank()
        return self._rank

    @property
    def score(self):
        if hasattr(self, '_score'):
            return self._score
        self._score = self.__get_score()
        return self._score

    def add(self, score):
        with self.redis.pipeline() as pipe:
            pipe.multi()
            pipe.zadd(self.key, score, self.user_id)
            self._rank = self.__get_rank(pipe)
            self._score = self.__score(pipe)

            pipe.execute()

    @classmethod
    def get_range(cls, key, begin, end, client=None, **kwargs):
        if not client:
            client = redis.StrictRedis(**kwargs)
        return client.zrevrange(key, begin - 1, end - 1, withscores=True)

    @classmethod
    def get_all(cls, key, client=None, **kwargs):
        if not client:
            client = redis.StrictRedis(**kwargs)
        return client.zrevrange(key, 0, -1, withscores=True)
