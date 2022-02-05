"""
A module that handles all default RESTful API actions for users
"""
from flask import jsonify, request
from app import db
from app.models import User
from app.api import bp


# route that retrieves a particular user account
@bp.route('/user/<string:name>', methods=['GET'], strict_slashes=False)
def get_user(name):
    pass


# create api route that creates a book resource
@bp.route('/user/<string:name>', methods=['POST'], strict_slashes=False)
def create_user(name):
    pass


# route that updates particular info about a user
@bp.route('/user/<string:name>', methods=['PUT'], strict_slashes=False)
def update_user(name):
    pass


# route that deletes a particular user account
@bp.route('/user/<string:name>', methods=['DELETE'], strict_slashes=False)
def delete_user(name):
    pass