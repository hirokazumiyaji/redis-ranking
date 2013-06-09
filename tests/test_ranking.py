# coding: utf-8

import random
import unittest
import redis

from ranking import Ranking


class RankingTest(unittest.TestCase):

    def setUp(self):
        self.client = redis.StrictRedis()
        self.client.flushdb()

        self.ranking_data = {'user{}'.format(i): random.randint(1, 100) for i in range(1, 11)}
        self.sorted_ranking_data = sorted([{'user_id': k, 'score': v} for k, v in self.ranking_data.items()],
                                          key=lambda x: x['score'], reverse=True)

        for k, v in self.ranking_data.items():
            self.client.zadd('ranking', v, k) 

    def tearDown(self):
        self.client.flushdb()

    def test_rank(self):
        ranking = Ranking('ranking', 'user1')
        rank = 0
        for i, data in enumerate(self.sorted_ranking_data):
            if data['user_id'] == 'user1':
                rank = i + 1
                break

        self.assertEqual(ranking.rank, rank)

    def test_score(self):
        ranking = Ranking('ranking', 'user1')
        score = 0
        for i, data in enumerate(self.sorted_ranking_data):
            if data['user_id'] == 'user1':
                score = data['score']
                break

        self.assertEqual(ranking.score, score)

    def test_get_range(self):
        ranking = Ranking.get_range('ranking', 1, 5)
        self.assertEqual(len(ranking), 5)
        for i, r in enumerate(ranking):
            self.assertEqual(r[0], self.sorted_ranking_data[i]['user_id'])
            self.assertEqual(r[1], self.sorted_ranking_data[i]['score'])

    def test_get_all(self):
        ranking = Ranking.get_all('ranking')
        self.assertEqual(len(ranking), 10)
        for i, r in enumerate(ranking):
            self.assertEqual(r[0], self.sorted_ranking_data[i]['user_id'])
            self.assertEqual(r[1], self.sorted_ranking_data[i]['score'])

if __name__ == '__main__':
    unittest.main()
