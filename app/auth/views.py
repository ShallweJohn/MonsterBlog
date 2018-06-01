from flask import redirect, url_for, render_template, session, current_app, request, flash
from flask_login import login_user, logout_user

from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('你现在可以登录')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    # 获取登陆表单对象
    form = LoginForm()
    # 验证表单提交情况
    if form.validate_on_submit():
        # 查询邮箱
        user = User.query.filter_by(email=form.email.data).first()
        # 验证用户名邮箱是否存在，验证密码
        if user is not None and user.verify_password(form.password.data):
            # 调用内建login_user函数，标记为已登陆用户
            login_user(user, form.remember_me.data)
            #
            return redirect(request.args.get('next')) or url_for('main.index')
        # 电子邮件或密码不正确，发送flash消息，再次渲染表单，让用户重试登陆
        flash('账户或密码不正确')
    return render_template('auth/login.html',form=form)



@auth.route('/logout')
def logout():
    logout_user()
    flash('你已登出')
    return redirect(url_for('main.index'))

