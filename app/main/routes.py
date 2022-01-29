"""
A module that handles the routes of the main part of the app
"""
from flask import render_template
from flask_login import login_required
from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """
    Route returns the home page of the application
    """
    return render_template('main/index.html', title="Home")
