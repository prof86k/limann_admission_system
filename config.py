import os


class Config(object):
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kkumasampson@gmail.com'
    MAIL_PASSWORD = ''
    MAIL_SUBJECT_PREFIX = 'ADMISSION OFFICE'
    MAIL_SENDER = 'kkumasampson@gmail.com'


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///admission_database.db'
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xfa\xe8\x8bH\xac5]\xee\xfb\xcd\xc1\x15\xf2\x8fl\x19\xb6'
    DEBUG = True
    ENV = 'Development'
    # FLASK_APP = "manage.py"


class ProdConfig(Config):
    MAIL_SERVER = 'wtu.edu.gh'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'noreply.admissions@wtu.edu.gh'
    MAIL_PASSWORD = 'Noreply@123'
    MAIL_SUBJECT_PREFIX = 'ADMISSION SYSTEM'
    MAIL_SENDER = 'noreply.admissions@wtu.edu.gh'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://ngs:Ngsappdb123$@localhost/admission_limann'
    SECRET_KEY = b'\xfa\xe8\x8bH\xac5]\xee\xfb\xcd\xc1\x15\xf2\x8fl\x19\xb6'
    DEBUG = False
    ENV = 'production'
