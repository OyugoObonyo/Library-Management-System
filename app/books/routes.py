"""
A module that contains routes related to the book blueprint
"""
from turtle import title
from app import db
from flask import flash, redirect, render_template, request
from app.models import Book
from app.books import bp


@bp.route('/books/s/<name>')
def get_book(name):
    """
    A route that displays a particular book with a particular id
    the route renders a book page in case it's successful
    """
    book = Book.query.filter_by(Book.title == name)
    # Return flash message and redirect to requesting page if name isn't found
    if book is None:
        flash("Sorry, book is unavailable at the moment")
        return redirect(request.referrer)
    return render_template('books/book.html', book=book)


@bp.route('/show-book/<id>')
def show_book(id):
    """
    A route that renders book details to a user
    """
    book = Book.query.filter_by(id=id).first()
    title = book.title
    return render_template('books/show_book.html', title=title, book=book)


@bp.route('/borrow/<id>', methods=['GET', 'POST'])
def borrow_book(id):
    """
    A route that handles borrowing the book
    borrower's id and book's id is added to the user_book association table
    """
    pass


@bp.route('/return/<id>', methods=['GET', 'POST'])
def return_book(id):
    """
    A user can return a book they're done reading
    The route clears the book and user id from the association table
    """
    pass
