from flask_wtf import Form
from wtforms import PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app.models import User


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                            Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    # 通过使用WTForms提供的Regexp正则功能验证用户名格式
    username = StringField('Username',validators=[
        DataRequired(), Length(1, 64),Regexp('^[A-Za-z][A-Za-z0-9_.] *$', 0,
                                            'Usernames must have only letters,'
                                            'numbers, dots or underscores'
                                            )])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwrods must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    # 分别验证邮箱 和 用户名是否已存在
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')
