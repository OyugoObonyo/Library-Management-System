"""
A module with classes serving as database tables
"""
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """
    A class that represents the user table in the database
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        """
        A method that generates a password hash from users' passwords
        Takes a password as an arguement and sets the hashed password as the password hash
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        A method that confirms confirms a hash is assigned to the correct password
        return True if the hash matches the password and flase if it doesn't
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Returns a string representation of a user object
        """
        return f"<User_id: {self.id}, User_name: {self.name}>"


@login.user_loader
def load_user(id):
    """
    A user loader function that aids flask in geting user id for login
    returns the user id
    """
    return User.query.get(int(id))
