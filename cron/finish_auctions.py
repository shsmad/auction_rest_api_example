#/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
app_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../')
sys.path.append(app_path)

from application.application import create_app
app = create_app('app.cfg', cronapp=True)
with app.app_context():
    import application.model as model

    data = model.auction_close_finished()
    if not data:
        sys.exit()

    mails = []
    for x in data:
        mail = model.mail_create(
            message='Auction closed: %s' % x['auction_id'],
            subject='Auction closed',
            sender=app.config.get('MAIL_USERNAME'),
            recipients=[x['email']]
        )
        mails.append(mail)
    model.mail_send(mails)
