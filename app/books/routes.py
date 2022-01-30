"""
A module that contains routes related to the book blueprint
"""
from flask import flash, redirect, render_template, request, url_for
from app.models import Book
from app.books import bp


@bp.route('/books/s/<name>')
def get_book(name):
    """
    A route that displays a particular book with a particular id
    """
    book = Book.query.filter_by(Book.title == name)
    # Return flash message and redirect to requesting page if name isn't found
    if book is None:
        flash("Sorry, book is unavailable at the moment")
        return redirect(request.referrer)
    return render_template('books/book.html', book=book)


@bp.route('/add_book/<id>', methods=['GET', 'POST'])
def add_book(id):
    """
    A route that adds a book to the database
    """
    pass


@bp.route('/delete_book/<id>', methods=['GET', 'DELETE'])
def delete_book(id):
    """
    
    """
