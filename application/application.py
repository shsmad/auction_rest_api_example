# -*- coding: utf-8 -*-

from flask import Flask
import os
from threading import Thread
import logging
logging.basicConfig(level=logging.DEBUG)


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def create_app(cfg_filename, cronapp=False):
    """
    Основное приложение
    """
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    cfg = os.path.join(
        os.path.split(os.path.split(__file__)[0])[0], 'config', cfg_filename
    )
    app.config.from_pyfile(cfg)

    if cronapp:
        return app

    with app.app_context():
        from bp.account import bpaccount
        from bp.auction import bpauction

    app.register_blueprint(bpaccount, url_prefix='/api/v1.0')
    app.register_blueprint(bpauction, url_prefix='/api/v1.0')

    return app
