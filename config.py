"""
A module that contains the application's configuration variables
"""
import os

# get the app's root directory
root_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Assign the configuration variables as class variables of the config object
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key-for-development'
    # Add sqlite as development db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(root_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOK_IMAGES_DIR = 'static/images/books'
    # Limit maximum length of book cover image to 5MB
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

# os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)