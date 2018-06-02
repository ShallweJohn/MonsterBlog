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
    # 配置flask_session
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    PERMENANT_SESSION_LIFETIME = 86400 * 7

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'jiangloyalmyself@163.com'
    MAIL_PASSWORD = 'jiangizhang92'
    MONSTER_MAIL_SUBJECT_PREFIX = '[MONSTER]'
    MONSTER_MAIL_SENDER = 'MONSTER Admin <jiangloyalmyself@163.com>'
    MONSTER_ADMIN = os.environ.get('MONSTER_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass
    # 配置日志登记
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.ERROR

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}





















