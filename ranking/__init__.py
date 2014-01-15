# coding: utf-8

from .model import Ranking


def get_rank(conn, key, unique_id):
    return Ranking(key, conn).get_rank(unique_id)


def get_range(conn, key, begin, end):
    return Ranking(key, conn).get_range(begin, end)


def get_score(conn, key, unique_id):
    return Ranking(key, conn).get_score(unique_id)


def get_all(conn, key):
    return Ranking(key, conn).get_all()
