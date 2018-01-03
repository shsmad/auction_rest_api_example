# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from flask import current_app
from ..model import cfg


def mail_send(mails):
    s = smtplib.SMTP(cfg.get('MAIL_SERVER'), cfg.get('MAIL_PORT'))
    if current_app.config.get('MAIL_USERNAME'):
        s.login(cfg.get('MAIL_USERNAME'), cfg.get('MAIL_PASSWORD'))
    for mail in mails:
        s.sendmail(*mail)
    s.quit()


def mail_create(message, subject, sender, recipients):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['To'] = ', '.join(recipients)
    msg['From'] = sender
    return (sender, recipients, msg.as_string())
