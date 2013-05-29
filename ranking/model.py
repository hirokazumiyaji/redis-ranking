# coding: utf-8

import redis


class Ranking(object):

    def __init__(self, key, user_id, **kwargs):
        self.key = key
        self.user_id = user_id
        self.redis = redis.StrictRedis(**kwargs)

    def __get_rank(self, redis=None):
        if not redis:
            redis = self.redis
        return redis.zrerank(self.key, self.user_id)

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
            pipe.zadd(self.key, self.user_id, score)
            self._rank = self.__get_rank(pipe)
            self._score = self.__score(pipe)

            pipe.execute()

    @classmethod
    def get_range(cls, begin, end):
        pass

    @classmethod
    def get_all(cls):
        pass
