from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('无法获取该属性')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 确认用户账户
    # generate_confirmation_token（）生成令牌
    def generate_confirmation_token(self, expiration=3600):
        # 生成具有过期时间的json web签名
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # dump() 为指定的数据生成加密签名，
        # 然后数据和签名 序列化 生成令牌字符串
        return s.dumps({'confirm': self.id})

    # confirm（）检验令牌
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # load()解码令牌，唯一参数：令牌字符串。
            # 首先检验签名、过期时间，
            # 通过：返回数据；反之：抛出异常
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            return False
        # 检验通过
        # 检验令牌中的id和current_USER中的用户匹配，确保恶意用户并不能确认别人账户
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
