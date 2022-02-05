"""
A module that handles all default RESTful API actions for books
"""
from flask import jsonify, request, make_response, abort
from app import db
from app.models import Book
from app.api import bp


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
@bp.route('/books/update/<int:id>', methods=['PUT'], strict_slashes=False)
def update_book(id):
    if request.is_json:
        book = Book.query.get(id)
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


# api route that deletes a book
@bp.route('/books/delete/<int:id>', methods=['DELETE'], strict_slashes=False)
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return make_response(jsonify({"error": "Book does not exist"}), 404)

    db.session.delete(book)
    db.session.commit()
    return make_response(jsonify({"Success": "Book successfully deleted"}), 200)
