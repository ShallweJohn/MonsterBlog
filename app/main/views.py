from flask import render_template, current_app, abort
from app.main import main
from app.models import User


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

