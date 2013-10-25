# coding: utf-8
import logging
import redis


logger = logging.getLogger('redis_ranking')


class Ranking(object):
    EXPIRE = 60 * 60 * 24 * 14  # two week

    def __init__(self, key, unique_id, client=None, **kwargs):
        self.key = key
        self.unique_id = unique_id
        if client:
            self.client = client
        else:
            self.client = redis.StrictRedis(**kwargs)

        score = kwargs.get('score', None)
        if score:
            self._score = score

        rank = kwargs.get('rank', None)
        if rank:
            self._rank = rank

    def __get_rank(self):
        score = self.score
        count = self.client.zcount(self.key, score + 1, '+inf')
        logger.debug('rank\tunique_id:{}\trank:{}'.format(self.unique_id,
                                                          count + 1))
        return count + 1

    def __get_score(self):
        score = self.client.zscore(self.key, self.unique_id)
        self.expire()
        logger.debug('score\tuniques_id:{}\tscore:{}'.format(self.unique_id,
                                                             score))
        return score

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
        with self.client.pipeline() as pipe:
            pipe.multi()
            pipe.zadd(self.key, score, self.unique_id)
            self.expire(pipe)
            pipe.execute()

        self._rank = self.__get_rank(pipe)
        self._score = self.__score(pipe) 

    @classmethod
    def get_range(cls, key, begin, end, client=None, **kwargs):
        if not client:
            client = redis.StrictRedis(**kwargs)

        range_data = client.zrevrange(key, begin - 1, end -1, withscores=True)
        if cls.EXPIRE:
            client.expire(key, cls.EXPIRE)
        return [cls(key, unique_id, client=client, score=score)
                for unique_id, score in range_data]

    @classmethod
    def get_all(cls, key, client=None, **kwargs):
        if not client:
            client = redis.StrictRedis(**kwargs)

        # zrevrange key, 0, -1
        return cls.get_range(key, 1, 0, client=client, **kwargs)

    def expire(self, client=None):
        if not self.EXPIRE:
            return

        if not client:
            client = self.client
        client.expire(self.key, self.EXPIRE)
