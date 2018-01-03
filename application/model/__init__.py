# -*- coding: utf-8 -*-

from flask import current_app
from contextlib import contextmanager
import urlparse
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
import logging

url = urlparse.urlparse(current_app.config.get('DATABASE_URL'))

pool = ThreadedConnectionPool(
    1, 20, database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cfg = current_app.config


@contextmanager
def db_connection():
    try:
        con = pool.getconn()
        yield con
    finally:
        pool.putconn(con)


@contextmanager
def db_cursor(commit=False):
    with db_connection() as con:
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            yield cur
            if commit:
                con.commit()
        except psycopg2.DatabaseError as e:
            logging.getLogger(__name__).error('Error during using db: %s', e)
            con.rollback()
        finally:
            cur.close()


from account import (
    get_user_by_token, account_register, account_login, account_get,
    account_list
)
from auction import (
    auction_list, auction_create, auction_get,
    auction_get_bids, auction_place_bid,
    auction_close_finished, auction_bidders_list
)
from mail import mail_create, mail_send
