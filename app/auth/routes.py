"""
A module that handles authentication and authorization views
"""
from flask import redirect, render_template, url_for, flash, request
from app.auth import bp
from flask_login import login_required, login_user, logout_user, current_user
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.urls import url_parse
from app import db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route that handles logging users in
    """
    # Handle a situation where a user who's logged in hits the login route
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        # Validate if user doesn't exist or pasword is wrong
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        # Parse the url to find out the page user is to be referred to
        next_page = request.args.get('next')
        # Check if next page is empty or if network location is not empty
        # a non-empty network location might suggest that user is being referred to an external page
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Log In', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route that handles registration of new users to the system
    """
    # Handle a situation where a user who's logged in hits the register route
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! Registration was successful', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title="Register", form=form)


@bp.route('/logout')
@login_required
def logout():
    """
    Route that handles logging users out
    """
    logout_user()
    return render_template('auth/login.html', title='Log In')
