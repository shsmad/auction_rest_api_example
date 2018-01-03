# -*- coding: utf-8 -*-

from ..model import db_cursor


def auction_list(status=None):
    if status not in ('active', 'finished'):  # active, finished
        status = None

    with db_cursor() as cur:
        sql = """
        SELECT a.id,
        CASE WHEN a.finish_date > now() THEN 'active' ELSE 'finished' END AS status
        FROM auctions a
        """
        if status:
            sql = """
            SELECT af.id, af.status from (%s) as af
            WHERE af.status=%%s
            """ % sql
        cur.execute(sql, (status, ))

        auctions = cur.fetchall()
        return auctions


def auction_create(account_id, description, bid_start, bid_step, finish_date):
    with db_cursor(commit=True) as cur:
        sql = """
        INSERT INTO auctions (description, bid_start, bid_step, finish_date, account_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        cur.execute(sql, (description, bid_start, bid_step, finish_date, account_id))

        auction = cur.fetchone()
        return auction


def auction_get(auction_id):
    with db_cursor() as cur:
        sql = """
        SELECT a.id,
        CASE WHEN a.finish_date > now() THEN 'active' ELSE 'finished' END AS status,
        a.description, a.bid_start, a.bid_step, a.finish_date, a.account_id
        FROM auctions a
        WHERE a.id = %s
        """
        cur.execute(sql, (auction_id, ))
        auction = cur.fetchone()
        return auction


def auction_get_bids(auction_id):
    with db_cursor() as cur:
        sql = """
        SELECT b.bid_date, b.bid_value, ac.username
        FROM bids b
        JOIN auctions a ON a.id = b.auction_id AND b.auction_id=%s
        JOIN accounts ac on ac.id=b.account_id
        """
        cur.execute(sql, (auction_id, ))
        bids = cur.fetchall()
        return bids


def auction_place_bid(auction_id, bid, account_id):
    with db_cursor(commit=True) as cur:
        sql = """
        INSERT INTO bids (account_id, auction_id, bid_value)
        VALUES (%s, %s, %s)
        RETURNING id, bid_value
        """
        cur.execute(sql, (account_id, auction_id, bid))
        bid = cur.fetchone()
        return bid


def auction_close_finished():
    with db_cursor(commit=True) as cur:
        auctions = set()
        sql = """
        UPDATE auctions a
        SET win_bid_id = b.id
        FROM bids b
        JOIN (
            SELECT auction_id, MAX(bid_value) AS bid_value FROM bids GROUP BY auction_id
        ) b2 ON b.auction_id = b2.auction_id AND b.bid_value=b2.bid_value
        WHERE a.win_bid_id IS NULL AND a.finish_date < now() AND b.auction_id = a.id
        RETURNING a.id, a.win_bid_id
        """
        cur.execute(sql)
        closed_auctions = cur.fetchall()
        for a in closed_auctions:
            auctions.add(str(a['id']))
        if not auctions:
            return []
        sql = """
        SELECT DISTINCT b.auction_id, a.email
        FROM accounts a
        JOIN bids b ON a.id = b.account_id
        WHERE b.auction_id IN (%s)
        group by b.auction_id, a.email
        """ % ', '.join(auctions)
        cur.execute(sql)
        emails = cur.fetchall()
        return emails


def auction_bidders_list(auction_id):
    with db_cursor() as cur:
        sql = """
        SELECT DISTINCT a.id, a.username, a.email
        FROM accounts a
        JOIN bids b ON b.account_id = a.id AND b.auction_id = %s
        """
        cur.execute(sql, (auction_id, ))
        bidders = cur.fetchall()
        return bidders
