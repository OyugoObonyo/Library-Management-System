"""
A module that handles all default RESTful API actions for users
"""
from flask import jsonify, request, make_response, current_app
from app import db
from app.models import User
from app.api import bp
import jwt
from functools import wraps
import datetime


# check for token and provide access to user with valid tokens only
def check_for_token(func):
    """
    decorator function that works with the token
    """
    @wraps(func)
    # wrap function with any number of positional or keyword args
    def wrapped(*args, **kwargs):
        # initialize token with value of none
        token = None
        # check if token is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response(jsonify({"error": "token is missing"}), 401)

        try:
            # decode the jwt token if it exists
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            # query the user in the db whom the token belongs to
            current_user = User.query.filter_by(name=data['name']).first()
        except Exception as e:
            # return token invalid error in case token does not match
            return make_response(jsonify({"error": "token is invalid"}), 401)
        # pass user object along with positional and kw args to the route in case token is correct
        return func(current_user, *args, **kwargs)
    return wrapped


@bp.route('/token', strict_slashes=False)
def token():
    """
    route that enables users to get jwt tokens unique to each user
    """
    # get authorization data
    auth = request.authorization

    # check if any auth components are missing
    if not auth or not auth.username or not auth.password:
        return make_response(jsonify({"error": "Verification has failed"}), 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    user = User.query.filter_by(name=auth.username).first()
    # return error if user does not exist
    if not user:
        return make_response(jsonify({"error": "User doesn't exist, please register first"}), 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    if user.check_password(auth.password):
        token = jwt.encode({'name': user.name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
        return jsonify({'token': token})
    # return error if password is incorrect
    return make_response(jsonify({"error": "Verification has failed, password is incorrect"}), 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@bp.route('/users', methods=['GET'], strict_slashes=False)
@check_for_token
def get_users(current_user):
    """
    Retrieves all user account details
    """
    # handle the off chance that a user trying to consume this API is anonymous
    if current_user is None:
        return make_response(jsonify({"error": "action not allowed for this user"}), 403)
    if not current_user.is_admin:
        return make_response(jsonify({"error": "action not allowed for this user"}), 403)
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


@bp.route('/users/count', methods=['GET'], strict_slashes=False)
@check_for_token
def number_users(current_user):
    """
    Returns the total number of users in the database
    """
    if current_user is None:
        return make_response(jsonify({"error": "action not allowed for this user"}), 403)
    if not current_user.is_admin:
        return make_response(jsonify({"error": "action not allowed for this user"}), 403)
    users_count = User.query.count()
    return jsonify({"Total number of books": users_count})


@bp.route('/user/<int:id>', methods=['GET'], strict_slashes=False)
@check_for_token
def get_user(current_user, id):
    """
    Retrieves a user with a particular id from the database
    """
    # handle the off chance that a user trying to consume this API is anonymous
    if current_user is None:
        return make_response(jsonify({"error": "action not allowed for this user"}), 403)
    if not current_user.is_admin:
        return make_response(jsonify({"error": "action not allowed for this user"}), 403)
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
def create_user(current_user):
    """
    Creates a user in the database
    """
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
@bp.route('/user/update', methods=['PUT'], strict_slashes=False)
@check_for_token
def update_user(current_user):
    """
    Updates a user's information in the database
    """
    # handle the off chance that a user trying to consume this API is anonymous
    if current_user is None:
        return make_response(jsonify({"error": "action not allowed for this user"}), 403)
    if request.is_json:
        ignore = ['id', 'password_hash', 'is_admin']
        data = request.get_json()
        # Make sure user does not change email or name to an existing email or name
        check_email = User.query.filter_by(email=request.json['email']).first()
        check_user = User.query.filter_by(name=request.json['name']).first()
        if check_email or check_user:
            return make_response(jsonify({"error": "An account with that username or email already exists"}), 400)
        for key, value in data.items():
            if key not in ignore:
                setattr(current_user, key, value)
        db.session.commit()
        return make_response(jsonify({"Success": "User account succesfully updated"}), 200)
    else:
        return make_response(jsonify({"error": "Input not a JSON"}), 400)


# route that deletes a particular user account
@bp.route('/user/<int:id>', methods=['DELETE'], strict_slashes=False)
@check_for_token
def delete_user(current_user, id):
    """
    Deletes a user from the database
    """
    # handle the off chance that a user trying to consume this API is anonymous
    if current_user is None:
        return make_response(jsonify({"error": "action not allowed for this user"}), 403)
    if not current_user.is_admin:
        return make_response(jsonify({"error": "action not allowed for this user"}), 403)
    user = User.query.get(id)
    if user is None:
        return make_response(jsonify({"error": "User does not exist"}), 404)

    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({"Success": "User successfully deleted"}), 200)
