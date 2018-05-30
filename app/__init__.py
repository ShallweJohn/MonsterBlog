import redis
import logging
from logging.handlers import RotatingFileHandler
from flask_bootstrap import Bootstrap
from flask import Flask
from flask_session import Session
from flask_login import LoginManager
from config import Config
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment


db = SQLAlchemy()
redis_store = None
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
login_manager = LoginManager()

# LogingManager对象的session_protection属性可以设为None，basic，strong
# 以提供不同的安全防护等级
#

login_manager.session_protection = 'strong'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):

    app = Flask(__name__)
    bootstrap.init_app(app)
    app.config.from_object(Config)
    CSRFProtect(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    global redis_store
    redis_store = redis.StrictRedis(host=config_name.REDIS_HOST, port=config_name.REDIS_PORT)
    Session(app)
    setup_log(config_name)

    # 导入并注册蓝图main
    from app.main import main
    app.register_blueprint(main)
    # 导入并注册蓝图auth
    from app.auth import auth
    app.register_blueprint(auth)

    return app


def setup_log(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=config_name.LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
