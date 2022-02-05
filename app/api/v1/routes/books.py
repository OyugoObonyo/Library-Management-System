"""
A module that handles all default RESTful API actions for books
"""
from flask import jsonify, request, make_response, abort
from app import db
from app.models import Book
from app.api import bp


# api test
@bp.route('/test', methods=['GET'], strict_slashes=False)
def get_test():
    message = "Hello Test!"
    return jsonify({"message": message})


# route that returns a list of all books
@bp.route('/books', methods=['GET'], strict_slashes=False)
def get_books():
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


# route that returns the total number of books in the db
@bp.route('/book_count', methods=['GET'], strict_slashes=False)
def number_books():
    book_count = Book.query.count()
    return jsonify({"Total number of books": book_count})


# create route that returns a book with a particular name
# if book with name doesn't exist, return error messages
@bp.route('/books/<int:id>', methods=['GET'], strict_slashes=False)
def get_book(id):
    book = Book.query.get(id)
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


# api route that updates details of a particular book
@bp.route('/books/<int:id>', methods=['PUT'], strict_slashes=False)
def update_book(id):
    if request.is_json:
        book = Book.query.get(id)
        if book is None:
            return make_response(jsonify({"error": "Book does not exist"}), 404)

        if 'email' not in request.get_json():
            abort(400, description="Missing email")

        if 'password' not in request.get_json():
            abort(400, description="Missing password")

        book.title = request.json['title']
        book.synopsis = request.json['synopsis']


# api route that deletes a book
@bp.route('/books/<string:name>', methods=['DELETE'], strict_slashes=False)
def delete_book(name):
    pass