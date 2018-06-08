
from flask import render_template, current_app, abort, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from app import db
from app.decorators import admin_required
from app.main import main
from app.main.forms import EditProfileForm, EditProfileAdminForm
from app.models import User, Role
from utils.response_code import RET


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    try:
        user = User.query.filter_by(username=username).first()
    except Exception as e:
        current_app.logger.error(e)
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        try:
            db.session.add(current_user)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据库错误')

        # db.session.add(current_user)
        flash('你的个人资料已更新')

        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)



@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin():
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据库错误')
        flash('资料更新完成')
        return redirect('.user', username = user.username)
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

