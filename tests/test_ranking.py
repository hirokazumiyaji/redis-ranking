# coding: utf-8
from __future__ import unicode_literals
import random
import unittest
import redis

import ranking


class RankingTest(unittest.TestCase):

    def setUp(self):
        self.client = redis.StrictRedis()
        self.client.flushdb()

        self.ranking_data = [
            {'unique_id': str('user0'), 'score': 1000, 'rank': 8},
            {'unique_id': str('user1'), 'score': 1000, 'rank': 8},
            {'unique_id': str('user2'), 'score': 2000, 'rank': 6},
            {'unique_id': str('user3'), 'score': 3000, 'rank': 4},
            {'unique_id': str('user4'), 'score': 3000, 'rank': 4},
            {'unique_id': str('user5'), 'score': 4000, 'rank': 3},
            {'unique_id': str('user6'), 'score': 500, 'rank': 10},
            {'unique_id': str('user7'), 'score': 6000, 'rank': 1},
            {'unique_id': str('user8'), 'score': 1500, 'rank': 7},
            {'unique_id': str('user9'), 'score': 5000, 'rank': 2},
        ]

        for data in self.ranking_data:
            self.client.zadd('ranking', data['score'], data['unique_id'])

    def tearDown(self):
        self.client.flushdb()

    def test_rank(self):
        for data in self.ranking_data:
            self._test_rank(data)

    def _test_rank(self, data):
        rank = ranking.get_rank(self.client,
                                'ranking',
                                data['unique_id'])
        self.assertEqual(data['rank'], rank)

    def test_score(self):
        for data in self.ranking_data:
            self._test_score(data)

    def _test_score(self, data):
        score = ranking.get_score(self.client,
                                  'ranking',
                                  data['unique_id'])
        self.assertEqual(int(data['score']), int(score))

    def test_get_range(self):
        ranking_range = ranking.get_range(self.client,
                                          'ranking',
                                          1,
                                          5)
        self.assertEqual(len(ranking_range), 5)

    def test_get_all(self):
        ranking_all = ranking.get_all(self.client, 'ranking')
        self.assertEqual(len(ranking_all), 10)
        for i, ranking_data in enumerate(ranking_all):
            self.assertTrue('unique_id' in ranking_data)
            self.assertTrue('score' in ranking_data)

    def __get_data(unique_id):
        return next([data
                     for data in self.ranking_data
                     if data['unique_id'] == str(unique_id)],
                    data[0])

if __name__ == '__main__':
    unittest.main()
