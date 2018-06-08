from flask import redirect, url_for, render_template, session, current_app, request, flash
from flask_login import login_user, logout_user, current_user, login_required

from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.email import send_email
from app.models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # 获取注册表单对象
    form = RegistrationForm()
    # 验证提交情况
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '请确认你的账户', 'auth/email/confirm', user=user, token=token)
        flash('一封确认邮件已发送至你的邮箱')
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
            next = request.args.get('next')
            if next is None or not next.startwith('/'):
                next = url_for('main.index')
            return redirect(next)
        # 电子邮件或密码不正确，发送flash消息，再次渲染表单，让用户重试登陆
        flash('账户或密码不正确')
    return render_template('auth/login.html', form=form)

@auth.route('/confirm/<token>')
# 确认账户路由
# flask提供的login_required装饰器保护这个路由，先执行
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        return flash('你已确认过账户')
    else:
        flash('确认链接已失效过期')
        return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    """通过请求勾子处理过滤未确认账户"""
    if current_user.is_authenticated:
        current_user.refresh_last_seen()
        if not current_user.confirmed \
                and not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
# 重发验证电子邮件
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认你的账户',
               'auth/email/confirm', user = current_user, token=token)
    flash('一封确认邮件已发送至你的邮箱')
    return redirect(url_for('main.index'))

@auth.route('/logout')
def logout():
    logout_user()
    flash('你已登出')
    return redirect(url_for('main.index'))


