from flask import redirect, url_for, render_template, session, current_app, request, flash
from flask_login import login_user
from app.auth import auth
from app.auth.forms import LoginForm
from app.models import User




@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user,  form.remember_me.data)
            return redirect(request.args.get('next')) or url_for('main.index')
        flash('invalid username or password.')
    return render_template('auth/login.html',form=form)

        # next = request.args.get('next')
        #return redirect(request.args.get('next') or url_for('main'))
