import os
import redis
import logging


class Config(object):
    #配置数据库连接
    SQLALCHEMY_DATABASE_URI = 'mysql://root:19920917@127.0.0.1:3306/data_monster'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #配置redis数据库

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    SECRET_KEY = 'cpPnFCexQsC+keIFRtrM7jRdTY4B6N5EO1D0YTWu7H0='

    # 配置flask_session
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    PERMENANT_SESSION_LIFETIME = 86400 * 7

    # 配置日志登记
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.ERROR

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \'mysql:///'+is
























