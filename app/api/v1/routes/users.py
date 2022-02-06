"""
A module that handles all default RESTful API actions for users
"""
from logging import exception
from flask import jsonify, request, make_response, current_app
from app import db
from app.models import User
from app.api import bp
import jwt
from functools import wraps


@bp.route('/login', strict_slashes=False)
def login():
    auth = request.authorization
    if 


# check for token and provide access to user with valid tokens only
def check_for_token(func):
    @wraps(func)
    # wrap function with any number of positional or keyword args
    def wrapped(*args, **kwargs):
        # initialize token with value of none
        token = None
        # check if token is passed in the request header
        if 'x-access-token' in  request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response(jsonify({"error": "token is missing"}), 401)

        try:
            # decode the jwt token if it exists
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            # query the user in the db whom the token belongs to
            c_user = User.query.filter_by(id=data).first()
        except:
            # return token invalid error in case token does not match
            return make_response(jsonify({"error": "token is invalid"}), 401)

        # pass user object along with positional and kw args to the route in case token is correct
        return func(c_user, *args, **kwargs)
    return wrapped


# Retrieves all user accounts
@bp.route('/users', methods=['GET'], strict_slashes=False)
@check_for_token
def get_users(c_user):
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }
        user_list.append(user_data)
    return jsonify({"users": user_list})


# route that retrieves a particular user account
@bp.route('/user/<int:id>', methods=['GET'], strict_slashes=False)
@check_for_token
def get_user(c_user, id):
    user = User.query.get(id)
    if user is None:
        return make_response(jsonify({"error": "user does not exist"}), 404)
    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
    }
    return jsonify({"User": user_data})


# create api route that creates a user account
@bp.route('/user', methods=['POST'], strict_slashes=False)
@check_for_token
def create_user():
    if request.is_json:
        if 'name' not in request.get_json():
            return make_response(jsonify({"error": "name is missing"}), 400)
        if 'email' not in request.get_json():
            return make_response(jsonify({"error": "email is missing"}), 400)
        if 'password' not in request.get_json():
            return make_response(jsonify({"error": "password is missing"}), 400)

        user = User(
            name=request.json['name'],
            email=request.json['email']
        )
        check_user = User.query.filter_by(name=user.name).first()
        check_email = User.query.filter_by(email=user.email).first()
        if check_user is not None or check_email is not None:
            return make_response(jsonify({"error": "An account with that username or email already exists"}), 400)
        user.set_password(request.json['password'])
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"Success": "User successfully registered"}), 201)
    else:
        return make_response(jsonify({"error": "Input not a JSON"}), 400)


# route that updates particular info about a user
@bp.route('/user/<int:id>', methods=['PUT'], strict_slashes=False)
@check_for_token
def update_user(c_user, id):
    if request.is_json:
        user = User.query.get(id)
        if user is None:
            return make_response(jsonify({"error": "User does not exist"}), 404)

        ignore = ['id', 'password_hash', 'is_admin']
        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(user, key, value)
        db.session.commit()
        return make_response(jsonify({"Success": "User account succesfully updated"}), 200)
    else:
        return make_response(jsonify({"error": "Input not a JSON"}), 400)


# route that deletes a particular user account
@bp.route('/user/<int:id>', methods=['DELETE'], strict_slashes=False)
@check_for_token
def delete_user(c_user, id):
    user = User.query.get(id)
    if user is None:
        return make_response(jsonify({"error": "User does not exist"}), 404)

    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({"Success": "User successfully deleted"}), 200)
