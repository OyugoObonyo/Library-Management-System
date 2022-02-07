"""
A module that handles all default RESTful API actions for books
"""
from flask import jsonify, request, make_response, abort
from app import db
from app.models import Book
from app.api import bp
from app.api.v1.routes.users import check_for_token


@bp.route('/books', methods=['GET'], strict_slashes=False)
def get_books():
    """
    Retrieves all books from the database
    """
    books = Book.query.all()
    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'synopsis': book.synopsis,
            'Year of publishment': book.year_of_publish
        }
        book_list.append(book_data)
    return jsonify({"books": book_list})


@bp.route('/books/count', methods=['GET'], strict_slashes=False)
def number_books():
    """
    Retrieves the total number of books in the database
    """
    book_count = Book.query.count()
    return jsonify({"Total number of books": book_count})


@bp.route('/books/author', methods=['GET'], strict_slashes=False)
def book_author():
    """
    Retrieves books from a particular author in the db
    """
    # check if request is json
    if request.is_json:
        # ensure author is passed as parameter
        if 'author' not in request.get_json():
            return make_response(jsonify({"error": "author name is missing"}), 400)
        author = request.json['author']
        books = Book.query.filter_by(author=author).all()
        book_count = len(books)
        if book_count == 0:
            return jsonify({"message": "A book by this author doesn't currently exist"})
        books_list = []
        for book in books:
            book_data = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'synopsis': book.synopsis,
                'Year of publishment': book.year_of_publish
            }
            books_list.append(book_data)
        return jsonify({"author": author, "book_count": book_count, "books": books_list})
    else:
        return make_response(jsonify({"error": "Input not a JSON"}), 400)


@bp.route('/books/mine', methods=['GET'], strict_slashes=False)
@check_for_token
def user_books(current_user):
    """
    Returns the total number of books in the database
    """
    books = current_user.borrowed_books
    books_count = len(books)
    if books_count == 0:
        return jsonify({"message":"You haven't borrowed any book yet"})
    books_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'synopsis': book.synopsis,
            'Year of publishment': book.year_of_publish
        }
        books_list.append(book_data)
    return jsonify({"books_count": books_count, "books": books_list})


@bp.route('/books/<string:title>', methods=['GET'], strict_slashes=False)
def get_book(title):
    """
    Returns information about a book with a particular title
    """
    book = Book.query.filter_by(title=title).first()
    if book is None:
        return make_response(jsonify({"error": "Book does not exist"}), 404)
    book_data = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'synopsis': book.synopsis,
        'Year of publishment': book.year_of_publish
    }
    return jsonify({"Book": book_data})


@bp.route('/books/update/<string:title>', methods=['PUT'], strict_slashes=False)
@check_for_token
def update_book(current_user, title):
    """
    Updates a book resource in the database
    """
    # Make this API accessible to admin users only
    if not current_user.is_admin:
        return make_response(jsonify({"error": "Action not allowed for this user"}), 403)
    if request.is_json:
        book = Book.query.filter_by(title=title).first()
        if book is None:
            return make_response(jsonify({"error": "Book does not exist"}), 404)

        ignore = ['id', 'img_url']
        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(book, key, value)
        db.session.commit()
        return make_response(jsonify({"Success": "Book succesfully updated"}), 200)
    else:
        return make_response(jsonify({"error": "Input not a JSON"}), 400)


@bp.route('/books/delete/<string:title>', methods=['DELETE'], strict_slashes=False)
@check_for_token
def delete_book(current_user, title):
    """
    Deletes a book from the database
    """
    if not current_user.is_admin:
        return make_response(jsonify({"error": "action not allowed for this user"}), 403)
    book = Book.query.filter_by(title=title).first()
    if book is None:
        return make_response(jsonify({"error": "Book does not exist"}), 404)

    db.session.delete(book)
    db.session.commit()
    return make_response(jsonify({"Success": "Book successfully deleted"}), 200)
