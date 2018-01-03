# -*- coding: utf-8 -*-

from ..model import db_cursor
from hashlib import sha256
import uuid


def get_user_by_token(token):
    if token and token.startswith('Token '):
        token = token[6:]
        user = account_get(token=token)
        return user
    else:
        return None


def account_register(username, password, email):
    with db_cursor(commit=True) as cur:
        guid = uuid.uuid4()
        cur.execute("""
        INSERT INTO accounts (username, password, email, token)
        VALUES (LOWER(%s), %s, %s, %s)
        RETURNING id
        """, (
            username,
            sha256(password).hexdigest(),
            email,
            str(guid)
        ))

        res = cur.fetchone()
        return {'id': res['id'], 'token': str(guid)}


def account_login(username, password):
    with db_cursor() as cur:
        cur.execute("""
        SELECT a.id, a.username, a.email, a.token
        FROM accounts a
        WHERE LOWER(a.username) = LOWER(%s)
        AND a.password = %s
        """, (
            username,
            sha256(password).hexdigest()
        ))
        res = cur.fetchone()
        return res


def account_get(username=None, uid=None, token=None):

    if not username and not uid and not token:
        return None

    with db_cursor() as cur:

        if username:
            cur.execute("""
            SELECT a.id, a.username, a.email, a.token
            FROM accounts a
            WHERE LOWER(u.username) = LOWER(%s)
            """, (username, ))
        elif uid:
            cur.execute("""
            SELECT a.id, a.username, a.email, a.token
            FROM accounts a
            WHERE a.id = %s
            """, (uid, ))
        elif token:
            cur.execute("""
            SELECT a.id, a.username, a.email, a.token
            FROM accounts a
            WHERE a.token = %s
            """, (token, ))

        user = cur.fetchone()
        return user


def account_list():
    with db_cursor() as cur:
        sql = """
        SELECT a.id, a.username, a.email
        FROM accounts a
        """
        cur.execute(sql)
        users = cur.fetchall()
        return users
