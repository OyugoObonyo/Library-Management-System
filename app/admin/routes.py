"""
A module with routes associated to the auth blueprint
"""
import os
import uuid
import html
from app import db
from PIL import Image
from app.models import Book, User
from flask import current_app, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from app.admin import bp
from werkzeug.exceptions import RequestEntityTooLarge
from app.admin.forms import AddBookForm, UpdateBookForm


def check_admin():
    """
    A function that checks if a user is an administrator
    """
    if current_user.is_anonymous or not current_user.is_admin:
        abort(404)


@bp.route('/admin')
@login_required
def admin():
    """
    The route that renders the admin dashboard
    """
    check_admin()
    books = Book.query.all()
    return render_template('admin/index.html', title="Admin", books=books)


def save_image(image_file):
    """
    Function that saves an image to the filesystem
    takes image as an arguement
    returns the image's filename
    """
    # Generates random string and use it as image file name to ensure safe filenames
    image_id = str(uuid.uuid4())
    file_name = image_id + '.png'
    # Get full path of the image
    file_path = os.path.join(current_app.root_path, current_app.config['BOOK_IMAGES_DIR'], file_name)
    # Utilize IMage module from PIL library to manipulate image_file
    Image.open(image_file).save(file_path)
    # Return file name so as to save it as image url in the db
    return file_name


@bp.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    """
    A route that adds a book to the database
    """
    check_admin()
    form = AddBookForm()
    # Catch the case where image is larger than 5MB
    try:
        if form.validate_on_submit():
            image = form.image.data
            image_url = save_image(image)
            book = Book(title=form.title.data,
                        synopsis=html.unescape(form.synopsis.data),
                        author=form.author.data,
                        year_of_publish=form.year_of_publish.data,
                        img_url=image_url)
            db.session.add(book)
            db.session.commit()
            flash(f"{book.title} has been succesfully added to the library", "success")
            return redirect(url_for('admin.admin'))
    except RequestEntityTooLarge:
        raise "Maximum upload size allowed is 5MB"
    return render_template('books/create_book.html', title='Add a book', form=form)


@bp.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update_book(id):
    """
    A route that updates the properties of a particular book in the database
    """
    check_admin()
    book = Book.query.filter_by(id=id).first()
    form = UpdateBookForm()
    # Preload book values on CKeditor form
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.synopsis = form.synopsis.data
        book.year_of_publish = form.year_of_publish.data
        db.session.commit()
        flash(f"{book.title} has been succesfully updated", "success")
        return redirect(url_for('admin.admin'))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.synopsis.data = book.synopsis
        form.year_of_publish.data = book.year_of_publish
    return render_template('books/update_book.html', title='Update book details', form=form)


def delete_image(image_file):
    """
    Function that deletes a cover image from the file system
    """
    file_path = file_path = os.path.join(current_app.root_path, current_app.config['BOOK_IMAGES_DIR'], image_file)
    os.remove(file_path)


@bp.route('/delete-book/<id>', methods=['GET', 'DELETE'])
@login_required
def delete_book(id):
    """
    A route that handles deleting a book from the database
    It also deletes the book's cover image as well
    """
    check_admin()
    book = Book.query.filter_by(id=id).first()
    image_file = book.img_url
    delete_image(image_file)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('admin.admin'))
