"""
A module with auth forms as classes
"""
from flask_wtf import FlaskForm
from app.models import User
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField


class RegistrationForm(FlaskForm):
    """
    A class that inherits from the FlaskForm class and represents a registration form
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Validates form to check whether username already exists in the db
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Sorry, this Username is taken")

    def validate_email(self, email):
        """
        Validates form to check whether email already exists in the db
        """
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("Sorry, email already exists")


class LoginForm(FlaskForm):
    """
    A class that inherits from the Flaskform class and represents the loginform
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
