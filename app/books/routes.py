"""
A module that contains routes related to the book blueprint
"""
from flask_login import current_user
from app import db
from flask import flash, redirect, render_template, request
from app.models import Book, user_book, User
from app.books import bp


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
    book = Book.query.filter_by(id=id).first()
    user = User.query.filter_by(id=current_user.id).first()
    user.borrowed_books.append(book)
    db.session.commit()
    return redirect(request.referrer)


@bp.route('/return/<id>', methods=['GET', 'POST'])
def return_book(id):
    """
    A user can return a book they're done reading
    The route clears the book and user id from the association table
    """
    book = Book.query.filter_by(id=id).first()
    user = User.query.filter_by(id=current_user.id).first()
    user.borrowed_books.remove(book)
    db.session.commit()
    return redirect(request.referrer)


@bp.route('/my-books', methods=['GET'])
def my_books():
    """
    A route that renders a page showing all books borrowed by a particular user
    """
    books = current_user.borrowed_books
    library = len(books)
    return render_template('books/my_books.html', books=books, library=library)
