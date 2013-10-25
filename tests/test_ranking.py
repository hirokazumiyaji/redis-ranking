# coding: utf-8
import random
import unittest
import redis

from ranking import Ranking


class RankingTest(unittest.TestCase):

    def setUp(self):
        self.client = redis.StrictRedis()
        self.client.flushdb()

        self.ranking_data = {
            'user0': {'score': 1000, 'rank': 8},
            'user1': {'score': 1000, 'rank': 8},
            'user2': {'score': 2000, 'rank': 6},
            'user3': {'score': 3000, 'rank': 4},
            'user4': {'score': 3000, 'rank': 4},
            'user5': {'score': 4000, 'rank': 3},
            'user6': {'score': 500, 'rank': 10},
            'user7': {'score': 6000, 'rank': 1},
            'user8': {'score': 1500, 'rank': 7},
            'user9': {'score': 5000, 'rank': 2},
        }

        for k, v in self.ranking_data.items():
            self.client.zadd('ranking', v['score'], k)

    def tearDown(self):
        self.client.flushdb()

    def test_rank(self):
        for unique_id in self.ranking_data.keys():
            self._test_rank(unique_id)

    def _test_rank(self, unique_id):
        ranking = Ranking('ranking', unique_id)
        rank = self.ranking_data[unique_id]['rank']
        self.assertEqual(ranking.rank, rank)

    def test_score(self):
        for unique_id in self.ranking_data.keys():
            self._test_score(unique_id)

    def _test_score(self, unique_id):
        ranking = Ranking('ranking', unique_id)
        score = self.ranking_data[unique_id]['score']
        self.assertEqual(ranking.score, score)

    def test_get_range(self):
        ranking = Ranking.get_range('ranking', 1, 5)
        self.assertEqual(len(ranking), 5)

    def test_get_all(self):
        ranking = Ranking.get_all('ranking')
        self.assertEqual(len(ranking), 10)
        for i, r in enumerate(ranking):
            self.assertEqual(r.score,
                             self.ranking_data[r.unique_id]['score'])
            self.assertEqual(r.rank,
                             self.ranking_data[r.unique_id]['rank'])

if __name__ == '__main__':
    unittest.main()
