"""
A module that handles the routes of the main part of the app
"""
from flask import render_template
from flask_login import login_required
from app.main import bp
from app.models import Book, User


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """
    Route returns the home page of the application
    """
    books = Book.query.all()
    return render_template('main/index.html', title="Home", books=books)
