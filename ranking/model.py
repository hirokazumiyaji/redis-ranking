# coding: utf-8
from __future__ import unicode_literals
import redis


class Ranking(object):
    EXPIRE = 60 * 60 * 24 * 14  # two week

    def __init__(self, key, client=None, **kwargs):
        self.key = key
        self.client = client or redis.StrictRedis(**kwargs)

    def get_rank(self, unique_id):
        score = self.get_score(unique_id)
        count = self.client.zcount(self.key, score + 1, '+inf')
        return count + 1

    def get_score(self, unique_id):
        with self.client.pipeline(False) as pipeline:
            pipeline.zscore(self.key, unique_id)
            self.expire(pipeline)
            score, _ = pipeline.execute()
        return score

    def add(self, score):
        with self.client.pipeline(False) as pipeline:
            pipeline.zadd(self.key, score, self.unique_id)
            self.expire(pipeline)
            pipeline.execute()

    def get_range(self, begin, end):
        with self.client.pipeline(False) as pipeline:
            pipeline.zrevrange(self.key, begin - 1, end - 1, withscores=True)
            self.expire(pipeline)
            datas, _ = pipeline.execute()

        return [
            {"unique_id": unique_id, "score": score}
            for unique_id, score in datas
        ]

    def get_all(self):
        return self.get_range(1, 0)

    def expire(self, client=None):
        if not self.EXPIRE:
            return

        if not client:
            client = self.client
        client.expire(self.key, self.EXPIRE)
