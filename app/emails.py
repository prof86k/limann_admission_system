from flask import render_template
from flask_mail import Message
from threading import Thread


from . import mail, create_app
from ..config import ProdConfig as Config

app = create_app()


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def purchased_card_mail(to, subject, template, **kwargs):
    '''send the purchased card info to the email provided'''
    msg = Message(Config.MAIL_SUBJECT_PREFIX + subject, sender=Config.MAIL_SENDER, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_async_mail, args=[app, msg])
    thread.start()
    return thread


def application_submited_mail(to, subject, template, **kwargs):
    '''send information regarding the application on submited info'''
    msg = Message(Config.MAIL_SUBJECT_PREFIX + subject, sender=Config.MAIL_SENDER, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_async_mail, args=[app, msg])
    thread.start()
    return thread


def applicant_admitted(to, subject, template, **kwargs):
    '''if applicant is admitted send them an email of notification'''
    msg = Message(Config.MAIL_SUBJECT_PREFIX + subject, sender=Config.MAIL_SENDER, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_async_mail, args=[app, msg])
    thread.start()
    return thread
